"""Corrected examples for the weak generated-test review exercise.

These are examples, not the only valid answers.
"""


def test_create_item_returns_payload_fields(client):
    response = client.post("/work-items", json={"title": "x", "priority": "high"})
    body = response.json()
    assert response.status_code == 201
    assert body["title"] == "x"
    assert body["priority"] == "high"
    assert body["id"]


def test_filter_done_items_excludes_other_statuses(client):
    done = client.post("/work-items", json={"title": "A", "status": "done"}).json()
    client.post("/work-items", json={"title": "B", "status": "todo"})
    response = client.get("/work-items?status=done")
    assert response.status_code == 200
    assert [item["id"] for item in response.json()] == [done["id"]]


def test_delete_item_makes_follow_up_get_return_404(client):
    created = client.post("/work-items", json={"title": "Delete me"}).json()
    assert client.delete(f"/work-items/{created['id']}").status_code == 204
    assert client.get(f"/work-items/{created['id']}").status_code == 404
