from __future__ import annotations


def create_item(client, **overrides):
    payload = {
        "title": "Write tests",
        "description": "Cover the API behavior",
        "status": "todo",
        "priority": "medium",
        "assignee": "Ada",
    }
    payload.update(overrides)
    response = client.post("/work-items", json=payload)
    assert response.status_code == 201, response.text
    return response.json()


def test_health(client):
    assert client.get("/health").json() == {"status": "ok"}


def test_create_work_item_returns_payload_and_timestamps(client):
    item = create_item(client, title="Plan implementation", priority="high")

    assert item["id"]
    assert item["title"] == "Plan implementation"
    assert item["priority"] == "high"
    assert item["status"] == "todo"
    assert item["created_at"]
    assert item["updated_at"]


def test_rejects_empty_title(client):
    response = client.post("/work-items", json={"title": ""})

    assert response.status_code == 422


def test_list_work_items_empty_and_then_ordered(client):
    assert client.get("/work-items").json() == []

    first = create_item(client, title="A")
    second = create_item(client, title="B")

    listed = client.get("/work-items").json()

    assert [item["id"] for item in listed] == [first["id"], second["id"]]


def test_get_work_item_by_id_and_missing_returns_404(client):
    item = create_item(client, title="Find me")

    response = client.get(f"/work-items/{item['id']}")
    missing = client.get("/work-items/not-here")

    assert response.status_code == 200
    assert response.json()["title"] == "Find me"
    assert missing.status_code == 404


def test_patch_work_item_preserves_unspecified_fields(client):
    item = create_item(client, title="Original", status="todo", priority="medium", assignee="Ada")

    response = client.patch(f"/work-items/{item['id']}", json={"status": "in_progress"})
    updated = response.json()

    assert response.status_code == 200
    assert updated["id"] == item["id"]
    assert updated["title"] == "Original"
    assert updated["priority"] == "medium"
    assert updated["assignee"] == "Ada"
    assert updated["status"] == "in_progress"
    assert updated["updated_at"] >= item["updated_at"]


def test_patch_missing_item_returns_404(client):
    response = client.patch("/work-items/not-here", json={"status": "done"})

    assert response.status_code == 404


def test_delete_work_item_and_missing_item(client):
    item = create_item(client, title="Delete me")

    deleted = client.delete(f"/work-items/{item['id']}")
    after_delete = client.get(f"/work-items/{item['id']}")
    missing_delete = client.delete("/work-items/not-here")

    assert deleted.status_code == 204
    assert after_delete.status_code == 404
    assert missing_delete.status_code == 404


def test_filter_by_status(client):
    todo = create_item(client, title="Todo", status="todo")
    create_item(client, title="Done", status="done")

    response = client.get("/work-items?status=todo")
    items = response.json()

    assert response.status_code == 200
    assert [item["id"] for item in items] == [todo["id"]]


def test_filter_by_priority(client):
    high = create_item(client, title="High", priority="high")
    create_item(client, title="Low", priority="low")

    response = client.get("/work-items?priority=high")
    items = response.json()

    assert response.status_code == 200
    assert [item["id"] for item in items] == [high["id"]]


def test_combined_filter_status_and_priority(client):
    expected = create_item(client, title="Expected", status="todo", priority="high")
    create_item(client, title="Wrong status", status="done", priority="high")
    create_item(client, title="Wrong priority", status="todo", priority="low")

    response = client.get("/work-items?status=todo&priority=high")
    items = response.json()

    assert response.status_code == 200
    assert [item["id"] for item in items] == [expected["id"]]


def test_invalid_enum_values_return_422(client):
    response = client.post("/work-items", json={"title": "Bad", "status": "blocked"})

    assert response.status_code == 422
