from __future__ import annotations

import os
from datetime import date, datetime, timezone
from functools import lru_cache
from pathlib import Path
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query, Response, status
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from .models import WorkItem, WorkItemCreate, WorkItemUpdate, WorkItemView, WorkPriority, WorkStatus
from .overdue import is_overdue
from .repository import SQLiteWorkItemRepository, WorkItemRepository

app = FastAPI(title="Work Items API", version="0.4.0")
app.mount("/static", StaticFiles(directory=Path(__file__).parent / "static"), name="static")
DEFAULT_DB_PATH = Path(os.getenv("WORK_ITEMS_DB", "work_items.db"))


@lru_cache(maxsize=1)
def get_repository() -> WorkItemRepository:
    # Created on first use, so importing the app (for example in tests) never creates a database file.
    return SQLiteWorkItemRepository(DEFAULT_DB_PATH)


def server_now() -> datetime:
    """Return the current instant as an aware datetime in the server's own timezone.

    This is the single clock seam: a test can replace it with a fixed instant.
    """
    return datetime.now().astimezone()


def get_reference_date() -> date:
    """REQ-04: overdue is decided against the UTC calendar day, whatever the server's timezone."""
    return server_now().astimezone(timezone.utc).date()


def view(item: WorkItem, reference_date: date) -> WorkItemView:
    return WorkItemView(**item.model_dump(), overdue=is_overdue(item, reference_date))


@app.get("/", include_in_schema=False)
def home():
    return FileResponse(Path(__file__).parent / "static/index.html")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/work-items", response_model=WorkItemView, status_code=status.HTTP_201_CREATED)
def create_work_item(
    payload: WorkItemCreate,
    repository: Annotated[WorkItemRepository, Depends(get_repository)],
    reference_date: Annotated[date, Depends(get_reference_date)],
) -> WorkItemView:
    return view(repository.create_item(payload), reference_date)


@app.get("/work-items", response_model=list[WorkItemView])
def list_work_items(
    repository: Annotated[WorkItemRepository, Depends(get_repository)],
    reference_date: Annotated[date, Depends(get_reference_date)],
    status_filter: Annotated[WorkStatus | None, Query(alias="status")] = None,
    priority: WorkPriority | None = None,
    overdue_only: bool = False,
) -> list[WorkItemView]:
    items = [
        view(item, reference_date) for item in repository.list_items(status=status_filter, priority=priority)
    ]
    return [item for item in items if item.overdue] if overdue_only else items


@app.get("/work-items/{item_id}", response_model=WorkItemView)
def get_work_item(
    item_id: str,
    repository: Annotated[WorkItemRepository, Depends(get_repository)],
    reference_date: Annotated[date, Depends(get_reference_date)],
) -> WorkItemView:
    item = repository.get_item(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Work item not found")
    return view(item, reference_date)


@app.patch("/work-items/{item_id}", response_model=WorkItemView)
def update_work_item(
    item_id: str,
    payload: WorkItemUpdate,
    repository: Annotated[WorkItemRepository, Depends(get_repository)],
    reference_date: Annotated[date, Depends(get_reference_date)],
) -> WorkItemView:
    item = repository.update_item(item_id, payload)
    if item is None:
        raise HTTPException(status_code=404, detail="Work item not found")
    return view(item, reference_date)


@app.delete("/work-items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_work_item(
    item_id: str, repository: Annotated[WorkItemRepository, Depends(get_repository)]
) -> Response:
    if not repository.delete_item(item_id):
        raise HTTPException(status_code=404, detail="Work item not found")
    return Response(status_code=204)
