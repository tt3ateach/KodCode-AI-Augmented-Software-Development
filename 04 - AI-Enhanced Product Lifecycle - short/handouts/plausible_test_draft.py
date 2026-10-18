# Prepared AI-generated tests for review. Shown on screen only; not part of any test suite.
# Prompt used: "Write pytest tests for the overdue filter and the overdue rule."
from datetime import date

from app.models import WorkItem
from app.overdue import is_overdue


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


def test_overdue_flag_matches_the_rule_for_past_dates(client):
    """A task due yesterday gets the flag the overdue rule gives it."""
    created = client.post("/work-items", json={"title": "Past", "due_date": "2026-10-03"}).json()
    expected = is_overdue(WorkItem.model_validate(created), date.today())
    assert created["overdue"] == expected
