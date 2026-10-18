import sqlite3
from datetime import date

import pytest

from app.models import WorkItemCreate
from app.repository import SQLiteWorkItemRepository


@pytest.mark.parametrize(
    "due,status,expected",
    [
        ("2026-10-03", "todo", True),
        ("2026-10-03", "in_progress", True),
        ("2026-10-04", "todo", False),
        ("2026-10-05", "todo", False),
        (None, "todo", False),
        ("2026-10-03", "done", False),
    ],
)
def test_REQ_04_05_overdue_boundary(client, due, status, expected):
    response = client.post("/work-items", json={"title": "Review patch", "due_date": due, "status": status})
    assert response.status_code == 201
    item = response.json()
    assert item["overdue"] is expected
    assert client.get("/work-items/" + item["id"]).json()["overdue"] is expected


@pytest.mark.parametrize("invalid", ["2026-02-30", "04/10/2026", "2026-10-04T00:00:00Z", 0, "20261004", ""])
def test_REQ_02_invalid_date(client, invalid):
    assert client.post("/work-items", json={"title": "Bad date", "due_date": invalid}).status_code == 422


def test_REQ_01_03_omitted_and_null(client):
    created = client.post("/work-items", json={"title": "Write docs", "due_date": "2026-10-03"}).json()
    path = "/work-items/" + created["id"]
    retained = client.patch(path, json={"title": "Write better docs"}).json()
    assert retained["due_date"] == "2026-10-03"
    cleared = client.patch(path, json={"due_date": None}).json()
    assert cleared["due_date"] is None and cleared["overdue"] is False
    assert client.get(path).json()["due_date"] is None
    legacy = client.post("/work-items", json={"title": "Undated"}).json()
    assert legacy["due_date"] is None and legacy["overdue"] is False


def test_REQ_06_filter_actual_ids(client):
    ids = {}
    for title, status, due in [
        ("past", "todo", "2026-10-03"),
        ("today", "todo", "2026-10-04"),
        ("done", "done", "2026-10-03"),
        ("none", "todo", None),
    ]:
        ids[title] = client.post(
            "/work-items", json={"title": title, "status": status, "due_date": due}
        ).json()["id"]
    rows = client.get("/work-items?overdue_only=true").json()
    assert [row["id"] for row in rows] == [ids["past"]]
    assert client.get("/work-items?overdue_only=true&status=done").json() == []


def test_REQ_05_completion_and_reopen(client):
    item = client.post("/work-items", json={"title": "Finish", "due_date": "2026-10-03"}).json()
    path = "/work-items/" + item["id"]
    assert client.patch(path, json={"status": "done"}).json()["overdue"] is False
    assert client.patch(path, json={"status": "todo"}).json()["overdue"] is True


def test_REQ_07_existing_database_migrates_and_keeps_rows(tmp_path):
    path = tmp_path / "old.db"
    pre_feature_schema = """
        CREATE TABLE work_items (
            id TEXT PRIMARY KEY, title TEXT NOT NULL, description TEXT,
            status TEXT NOT NULL, priority TEXT NOT NULL, assignee TEXT,
            created_at TEXT NOT NULL, updated_at TEXT NOT NULL
        )
    """
    with sqlite3.connect(path) as conn:
        conn.execute(pre_feature_schema)
        conn.execute(
            "INSERT INTO work_items VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (
                "old-1",
                "Existing task",
                None,
                "todo",
                "medium",
                None,
                "2026-10-01T00:00:00+00:00",
                "2026-10-01T00:00:00+00:00",
            ),
        )
    repository = SQLiteWorkItemRepository(path)
    assert repository.get_item("old-1").due_date is None
    again = SQLiteWorkItemRepository(path)
    assert [item.id for item in again.list_items()] == ["old-1"]
    item = again.create_item(WorkItemCreate(title="New", due_date=date(2026, 10, 5)))
    assert again.get_item(item.id).due_date == date(2026, 10, 5)


def test_REQ_04_reference_day_changes_at_read_time(client):
    from app.main import app, get_reference_date

    item = client.post("/work-items", json={"title": "Daily", "due_date": "2026-10-04"}).json()
    path = "/work-items/" + item["id"]
    assert client.get(path).json()["overdue"] is False
    app.dependency_overrides[get_reference_date] = lambda: date(2026, 10, 5)
    assert client.get(path).json()["overdue"] is True


def test_existing_non_nullable_fields_reject_null(client):
    item = client.post("/work-items", json={"title": "Keep valid"}).json()
    for field in ["title", "status", "priority"]:
        assert client.patch("/work-items/" + item["id"], json={field: None}).status_code == 422
