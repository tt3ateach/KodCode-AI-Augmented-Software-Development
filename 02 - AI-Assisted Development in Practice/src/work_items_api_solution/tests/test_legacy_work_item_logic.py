from __future__ import annotations

from datetime import datetime

import pytest

from lab2_assets.legacy_work_item_logic import is_overdue, normalize_status


def test_normalize_status_aliases():
    assert normalize_status("new") == "todo"
    assert normalize_status("WIP") == "in_progress"
    assert normalize_status("completed") == "done"


def test_normalize_status_passes_unknown_values_through():
    assert normalize_status("Blocked") == "blocked"


def test_missing_due_date_is_not_overdue():
    assert is_overdue({"status": "todo"}, now=datetime(2026, 1, 2)) is False


def test_unfinished_past_due_item_is_overdue():
    item = {"status": "todo", "due_date": "2026-01-01"}

    assert is_overdue(item, now=datetime(2026, 1, 2)) is True


def test_done_item_is_not_overdue_even_when_due_date_is_past():
    item = {"status": "done", "due_date": "2026-01-01"}

    assert is_overdue(item, now=datetime(2026, 1, 2)) is False


def test_date_only_strings_are_interpreted_at_midnight():
    item = {"status": "todo", "due_date": "2026-01-02"}

    assert is_overdue(item, now=datetime(2026, 1, 2, 1, 0, 0)) is True


def test_malformed_date_raises_value_error():
    with pytest.raises(ValueError):
        is_overdue({"status": "todo", "due_date": "not-a-date"}, now=datetime(2026, 1, 2))
