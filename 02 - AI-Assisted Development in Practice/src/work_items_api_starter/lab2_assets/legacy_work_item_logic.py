from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

_STATUS_ALIASES = {
    "new": "todo",
    "open": "todo",
    "todo": "todo",
    "wip": "in_progress",
    "doing": "in_progress",
    "in progress": "in_progress",
    "in_progress": "in_progress",
    "complete": "done",
    "completed": "done",
    "done": "done",
}


def normalize_status(raw: str | None) -> str:
    """Normalize common partner status labels while passing unknown values through."""
    if raw is None:
        return "todo"
    cleaned = raw.strip().lower().replace("-", "_")
    return _STATUS_ALIASES.get(cleaned, cleaned)


def _parse_due(value: Any) -> datetime | None:
    if value is None or value == "":
        return None
    if isinstance(value, datetime):
        return value
    if isinstance(value, str):
        return datetime.fromisoformat(value)
    raise TypeError(f"Unsupported due date value: {type(value).__name__}")


def is_overdue(item: dict[str, Any], *, now: datetime | None = None) -> bool:
    """Return True when an unfinished item has a due date earlier than now."""
    if normalize_status(item.get("status")) == "done":
        return False
    due = _parse_due(item.get("due_at") or item.get("due_date"))
    if due is None:
        return False
    current = now or datetime.now(timezone.utc)
    if due.tzinfo is None and current.tzinfo is not None:
        current = current.replace(tzinfo=None)
    return due < current
