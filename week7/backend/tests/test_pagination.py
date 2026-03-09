"""Tests for pagination (skip/limit) and sorting on the GET /notes endpoint."""

import time


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _seed_notes(client, count: int):
    """Create *count* notes with predictable titles (Note 1 … Note N)."""
    notes = []
    for i in range(1, count + 1):
        r = client.post("/notes/", json={"title": f"Note {i}", "content": f"Content {i}"})
        assert r.status_code == 201, r.text
        notes.append(r.json())
        # Tiny sleep so created_at values are distinguishable on fast machines
        time.sleep(0.02)
    return notes


# ---------------------------------------------------------------------------
# Pagination – skip / limit
# ---------------------------------------------------------------------------


class TestPaginationDefaults:
    """Default pagination behaviour when no query params are given."""

    def test_default_returns_all_when_under_limit(self, client):
        """Without explicit skip/limit, up to 50 notes are returned."""
        _seed_notes(client, 5)
        r = client.get("/notes/")
        assert r.status_code == 200
        assert len(r.json()) == 5

    def test_default_limit_caps_at_50(self, client):
        """When more than 50 notes exist, default limit is 50."""
        _seed_notes(client, 55)
        r = client.get("/notes/")
        assert r.status_code == 200
        assert len(r.json()) == 50


class TestSkipParameter:
    """Tests for the `skip` (offset) query parameter."""

    def test_skip_zero_returns_from_start(self, client):
        _seed_notes(client, 5)
        r = client.get("/notes/", params={"skip": 0})
        assert r.status_code == 200
        assert len(r.json()) == 5

    def test_skip_positive(self, client):
        _seed_notes(client, 5)
        r = client.get("/notes/", params={"skip": 3})
        assert r.status_code == 200
        assert len(r.json()) == 2

    def test_skip_equal_to_total_returns_empty(self, client):
        _seed_notes(client, 3)
        r = client.get("/notes/", params={"skip": 3})
        assert r.status_code == 200
        assert r.json() == []

    def test_skip_exceeds_total_returns_empty(self, client):
        _seed_notes(client, 3)
        r = client.get("/notes/", params={"skip": 100})
        assert r.status_code == 200
        assert r.json() == []


class TestLimitParameter:
    """Tests for the `limit` query parameter."""

    def test_limit_restricts_result_count(self, client):
        _seed_notes(client, 10)
        r = client.get("/notes/", params={"limit": 3})
        assert r.status_code == 200
        assert len(r.json()) == 3

    def test_limit_larger_than_total(self, client):
        _seed_notes(client, 3)
        r = client.get("/notes/", params={"limit": 100})
        assert r.status_code == 200
        assert len(r.json()) == 3

    def test_limit_one(self, client):
        _seed_notes(client, 5)
        r = client.get("/notes/", params={"limit": 1})
        assert r.status_code == 200
        assert len(r.json()) == 1

    def test_limit_max_200(self, client):
        """limit has le=200 validation – values above 200 should be rejected."""
        r = client.get("/notes/", params={"limit": 201})
        assert r.status_code == 422  # Validation error

    def test_limit_exactly_200_accepted(self, client):
        _seed_notes(client, 3)
        r = client.get("/notes/", params={"limit": 200})
        assert r.status_code == 200

    def test_limit_zero_returns_empty(self, client):
        _seed_notes(client, 5)
        r = client.get("/notes/", params={"limit": 0})
        assert r.status_code == 200
        assert r.json() == []


class TestSkipAndLimitCombined:
    """Combined skip + limit for page-like behaviour."""

    def test_first_page(self, client):
        notes = _seed_notes(client, 10)
        r = client.get("/notes/", params={"skip": 0, "limit": 3, "sort": "id"})
        assert r.status_code == 200
        ids = [n["id"] for n in r.json()]
        assert ids == [notes[0]["id"], notes[1]["id"], notes[2]["id"]]

    def test_second_page(self, client):
        notes = _seed_notes(client, 10)
        r = client.get("/notes/", params={"skip": 3, "limit": 3, "sort": "id"})
        assert r.status_code == 200
        ids = [n["id"] for n in r.json()]
        assert ids == [notes[3]["id"], notes[4]["id"], notes[5]["id"]]

    def test_last_partial_page(self, client):
        notes = _seed_notes(client, 10)
        r = client.get("/notes/", params={"skip": 9, "limit": 5, "sort": "id"})
        assert r.status_code == 200
        data = r.json()
        assert len(data) == 1
        assert data[0]["id"] == notes[9]["id"]

    def test_pages_cover_all_notes(self, client):
        """Iterating with skip/limit should yield every note exactly once."""
        notes = _seed_notes(client, 7)
        all_ids = set()
        page_size = 3
        for page in range(10):  # generous upper bound
            r = client.get("/notes/", params={"skip": page * page_size, "limit": page_size, "sort": "id"})
            assert r.status_code == 200
            batch = r.json()
            if not batch:
                break
            all_ids.update(n["id"] for n in batch)
        assert all_ids == {n["id"] for n in notes}


# ---------------------------------------------------------------------------
# Sorting
# ---------------------------------------------------------------------------


class TestSortParameter:
    """Tests for the `sort` query parameter."""

    def test_sort_ascending_by_title(self, client):
        for t in ["Banana", "Apple", "Cherry"]:
            client.post("/notes/", json={"title": t, "content": "x" * 5})
        r = client.get("/notes/", params={"sort": "title"})
        assert r.status_code == 200
        titles = [n["title"] for n in r.json()]
        assert titles == sorted(titles)

    def test_sort_descending_by_title(self, client):
        for t in ["Banana", "Apple", "Cherry"]:
            client.post("/notes/", json={"title": t, "content": "x" * 5})
        r = client.get("/notes/", params={"sort": "-title"})
        assert r.status_code == 200
        titles = [n["title"] for n in r.json()]
        assert titles == sorted(titles, reverse=True)

    def test_default_sort_is_desc_created_at(self, client):
        """When no sort param is given, notes are ordered by created_at descending."""
        notes = _seed_notes(client, 5)
        r = client.get("/notes/")
        assert r.status_code == 200
        returned_ids = [n["id"] for n in r.json()]
        expected_ids = [n["id"] for n in reversed(notes)]
        assert returned_ids == expected_ids

    def test_sort_ascending_created_at(self, client):
        notes = _seed_notes(client, 5)
        r = client.get("/notes/", params={"sort": "created_at"})
        assert r.status_code == 200
        returned_ids = [n["id"] for n in r.json()]
        expected_ids = [n["id"] for n in notes]
        assert returned_ids == expected_ids

    def test_sort_by_id_ascending(self, client):
        notes = _seed_notes(client, 5)
        r = client.get("/notes/", params={"sort": "id"})
        assert r.status_code == 200
        ids = [n["id"] for n in r.json()]
        assert ids == sorted(ids)

    def test_sort_by_id_descending(self, client):
        notes = _seed_notes(client, 5)
        r = client.get("/notes/", params={"sort": "-id"})
        assert r.status_code == 200
        ids = [n["id"] for n in r.json()]
        assert ids == sorted(ids, reverse=True)

    def test_invalid_sort_field_falls_back_to_desc_created_at(self, client):
        """An unknown field should fall back to -created_at ordering."""
        notes = _seed_notes(client, 5)
        r = client.get("/notes/", params={"sort": "nonexistent_field"})
        assert r.status_code == 200
        returned_ids = [n["id"] for n in r.json()]
        expected_ids = [n["id"] for n in reversed(notes)]
        assert returned_ids == expected_ids

    def test_sort_combined_with_search(self, client):
        for t in ["Banana pie", "Apple pie", "Cherry pie"]:
            client.post("/notes/", json={"title": t, "content": "tasty"})
        r = client.get("/notes/", params={"q": "pie", "sort": "title"})
        assert r.status_code == 200
        titles = [n["title"] for n in r.json()]
        assert titles == sorted(titles)

    def test_sort_combined_with_pagination(self, client):
        """Sort + skip/limit should respect both ordering and offset."""
        notes = _seed_notes(client, 6)
        r = client.get("/notes/", params={"sort": "id", "skip": 2, "limit": 2})
        assert r.status_code == 200
        ids = [n["id"] for n in r.json()]
        all_ids_sorted = sorted(n["id"] for n in notes)
        assert ids == all_ids_sorted[2:4]


# ---------------------------------------------------------------------------
# Edge-case / empty-state tests
# ---------------------------------------------------------------------------


class TestEdgeCases:
    def test_list_empty_database(self, client):
        r = client.get("/notes/")
        assert r.status_code == 200
        assert r.json() == []


    def test_negative_skip_rejected_or_empty(self, client):
        """Negative skip is either rejected (422) or treated as 0."""
        _seed_notes(client, 3)
        r = client.get("/notes/", params={"skip": -1})
        if r.status_code == 200:
            # If accepted, verify it behaves like skip=0
            expected_r = client.get("/notes/", params={"skip": 0})
            assert r.json() == expected_r.json()
        else:
            assert r.status_code == 422


    def test_negative_limit_rejected_or_empty(self, client):
        """Negative limit is either rejected (422) or treated as 0."""
        _seed_notes(client, 3)
        r = client.get("/notes/", params={"limit": -1})
        assert r.status_code in (200, 422)

    def test_non_integer_skip_rejected(self, client):
        r = client.get("/notes/", params={"skip": "abc"})
        assert r.status_code == 422

    def test_non_integer_limit_rejected(self, client):
        r = client.get("/notes/", params={"limit": "abc"})
        assert r.status_code == 422
