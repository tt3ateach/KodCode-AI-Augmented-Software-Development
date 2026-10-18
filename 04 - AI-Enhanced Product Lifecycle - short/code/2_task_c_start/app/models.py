from __future__ import annotations

from datetime import date, datetime, timezone
from enum import Enum
from typing import Optional
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field, field_validator


class WorkStatus(str, Enum):
    todo = "todo"
    in_progress = "in_progress"
    done = "done"


class WorkPriority(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"


def calendar_date_only(value):
    if value is None or (isinstance(value, date) and not isinstance(value, datetime)):
        return value
    if not isinstance(value, str) or len(value) != 10:
        raise ValueError("Use a calendar date in YYYY-MM-DD format or null")
    try:
        parsed = date.fromisoformat(value)
    except ValueError as exc:
        raise ValueError("Use a valid calendar date in YYYY-MM-DD format") from exc
    if parsed.isoformat() != value:
        raise ValueError("Use YYYY-MM-DD format")
    return parsed


class WorkItemCreate(BaseModel):
    title: str = Field(min_length=1, max_length=120)
    description: Optional[str] = None
    status: WorkStatus = WorkStatus.todo
    priority: WorkPriority = WorkPriority.medium
    assignee: Optional[str] = None
    due_date: Optional[date] = None

    _validate_due_date = field_validator("due_date", mode="before")(calendar_date_only)


class WorkItemUpdate(BaseModel):
    @field_validator("title", "status", "priority", mode="before")
    @classmethod
    def non_nullable_fields(cls, value):
        if value is None:
            raise ValueError("This field cannot be null")
        return value

    title: Optional[str] = Field(default=None, min_length=1, max_length=120)
    description: Optional[str] = None
    status: Optional[WorkStatus] = None
    priority: Optional[WorkPriority] = None
    assignee: Optional[str] = None
    due_date: Optional[date] = None

    _validate_due_date = field_validator("due_date", mode="before")(calendar_date_only)


class WorkItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    title: str
    description: Optional[str]
    status: WorkStatus
    priority: WorkPriority
    assignee: Optional[str]
    created_at: datetime
    updated_at: datetime
    due_date: Optional[date] = None


class WorkItemView(WorkItem):
    overdue: bool


def new_work_item_id() -> str:
    return str(uuid4())


def utc_now() -> datetime:
    return datetime.now(timezone.utc)
