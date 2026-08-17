"""Intentionally weak generated-test draft for Module 2 review exercise.

Do not treat these as solution tests. Students should critique them.
"""


def test_create_item_returns_success(client):
    response = client.post("/work-items", json={"title": "x"})
    assert response.status_code < 400


def test_filter_done_items(client):
    client.post("/work-items", json={"title": "A", "status": "done", "priority": "medium"})
    response = client.get("/work-items?status=done")
    assert response.status_code == 200


def test_delete_item(client):
    created = client.post("/work-items", json={"title": "Delete me"}).json()
    response = client.delete(f"/work-items/{created['id']}")
    assert response.status_code == 204
