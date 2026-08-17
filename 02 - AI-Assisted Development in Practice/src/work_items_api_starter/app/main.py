from __future__ import annotations

import os
from pathlib import Path
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query, Response, status

from .models import WorkItem, WorkItemCreate, WorkItemUpdate, WorkPriority, WorkStatus
from .repository import SQLiteWorkItemRepository, WorkItemRepository

app = FastAPI(title="Work Items API", version="0.4.0")

DEFAULT_DB_PATH = Path(os.getenv("WORK_ITEMS_DB", "work_items.db"))
_default_repository = SQLiteWorkItemRepository(DEFAULT_DB_PATH)


def get_repository() -> WorkItemRepository:
    return _default_repository


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/work-items", response_model=WorkItem, status_code=status.HTTP_201_CREATED)
def create_work_item(
    payload: WorkItemCreate,
    repository: Annotated[WorkItemRepository, Depends(get_repository)],
) -> WorkItem:
    return repository.create_item(payload)


@app.get("/work-items", response_model=list[WorkItem])
def list_work_items(
    repository: Annotated[WorkItemRepository, Depends(get_repository)],
    status_filter: Annotated[WorkStatus | None, Query(alias="status")] = None,
    priority: WorkPriority | None = None,
) -> list[WorkItem]:
    return repository.list_items(status=status_filter, priority=priority)


@app.get("/work-items/{item_id}", response_model=WorkItem)
def get_work_item(
    item_id: str,
    repository: Annotated[WorkItemRepository, Depends(get_repository)],
) -> WorkItem:
    item = repository.get_item(item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Work item not found")
    return item


@app.patch("/work-items/{item_id}", response_model=WorkItem)
def update_work_item(
    item_id: str,
    payload: WorkItemUpdate,
    repository: Annotated[WorkItemRepository, Depends(get_repository)],
) -> WorkItem:
    item = repository.update_item(item_id, payload)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Work item not found")
    return item


@app.delete("/work-items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_work_item(
    item_id: str,
    repository: Annotated[WorkItemRepository, Depends(get_repository)],
) -> Response:
    deleted = repository.delete_item(item_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Work item not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
