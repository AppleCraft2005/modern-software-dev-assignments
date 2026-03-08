def test_get_note_not_found_returns_404(client):
    """GET /notes/999 should return 404 when the note does not exist."""
    r = client.get("/notes/999")
    assert r.status_code == 404
    data = r.json()
    assert data["detail"] == "Note not found"
