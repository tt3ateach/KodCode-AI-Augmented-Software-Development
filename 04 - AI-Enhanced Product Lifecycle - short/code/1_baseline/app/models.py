from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import Optional
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field


class WorkStatus(str, Enum):
    todo = "todo"
    in_progress = "in_progress"
    done = "done"


class WorkPriority(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"


class WorkItemCreate(BaseModel):
    title: str = Field(min_length=1, max_length=120)
    description: Optional[str] = None
    status: WorkStatus = WorkStatus.todo
    priority: WorkPriority = WorkPriority.medium
    assignee: Optional[str] = None


class WorkItemUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=120)
    description: Optional[str] = None
    status: Optional[WorkStatus] = None
    priority: Optional[WorkPriority] = None
    assignee: Optional[str] = None


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


def new_work_item_id() -> str:
    return str(uuid4())


def utc_now() -> datetime:
    return datetime.now(timezone.utc)
