# An AI-written test, shown on screen only. It is not part of the test suite.
# Prompt used: "Write a pytest test for the Overdue only filter."


def test_overdue_filter_returns_overdue_tasks(client):
    """Only unfinished past-due tasks appear in Overdue only."""
    for title, status, due in [
        ("past", "todo", "2026-10-03"),
        ("today", "todo", "2026-10-04"),
        ("done", "done", "2026-10-03"),
        ("none", "todo", None),
    ]:
        client.post("/work-items", json={"title": title, "status": status, "due_date": due})
    rows = client.get("/work-items?overdue_only=true").json()
    assert len(rows) == 1
