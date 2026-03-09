def test_create_complete_list_and_patch_action_item(client):
    payload = {"description": "Ship it"}
    r = client.post("/action-items/", json=payload)
    assert r.status_code == 201, r.text
    item = r.json()
    assert item["completed"] is False
    assert item["priority"] == "Medium"  # default priority
    assert item["due_date"] is None
    assert "created_at" in item and "updated_at" in item

    r = client.put(f"/action-items/{item['id']}/complete")
    assert r.status_code == 200
    done = r.json()
    assert done["completed"] is True

    r = client.get("/action-items/", params={"completed": True, "limit": 5, "sort": "-created_at"})
    assert r.status_code == 200
    items = r.json()
    assert len(items) >= 1

    r = client.patch(f"/action-items/{item['id']}", json={"description": "Updated"})
    assert r.status_code == 200
    patched = r.json()
    assert patched["description"] == "Updated"


def test_create_action_item_with_priority_and_due_date(client):
    payload = {"description": "Fix bug", "priority": "High", "due_date": "2026-03-15"}
    r = client.post("/action-items/", json=payload)
    assert r.status_code == 201
    item = r.json()
    assert item["priority"] == "High"
    assert item["due_date"] == "2026-03-15"


def test_patch_priority_and_due_date(client):
    r = client.post("/action-items/", json={"description": "Task"})
    item = r.json()
    assert item["priority"] == "Medium"

    r = client.patch(f"/action-items/{item['id']}", json={"priority": "Low", "due_date": "next week"})
    assert r.status_code == 200
    patched = r.json()
    assert patched["priority"] == "Low"
    assert patched["due_date"] == "next week"


def test_extract_endpoint(client):
    text = "TODO: write tests ASAP\nJust a note\nACTION: deploy by 2026-04-01"
    r = client.post("/action-items/extract", json={"text": text})
    assert r.status_code == 200
    items = r.json()
    assert len(items) == 2

    assert items[0]["description"] == "TODO: write tests ASAP"
    assert items[0]["priority"] == "High"
    assert items[0]["due_date"] is None

    assert items[1]["description"] == "ACTION: deploy by 2026-04-01"
    assert items[1]["due_date"] == "2026-04-01"


def test_extract_endpoint_empty_text(client):
    r = client.post("/action-items/extract", json={"text": "No action items here."})
    assert r.status_code == 200
    assert r.json() == []

