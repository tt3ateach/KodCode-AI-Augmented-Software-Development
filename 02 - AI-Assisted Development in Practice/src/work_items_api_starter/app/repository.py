from __future__ import annotations

import sqlite3
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Iterable

from .models import WorkItem, WorkItemCreate, WorkItemUpdate, WorkPriority, WorkStatus, new_work_item_id, utc_now


class WorkItemRepository(ABC):
    @abstractmethod
    def create_item(self, payload: WorkItemCreate) -> WorkItem: ...

    @abstractmethod
    def list_items(self, *, status: WorkStatus | None = None, priority: WorkPriority | None = None) -> list[WorkItem]: ...

    @abstractmethod
    def get_item(self, item_id: str) -> WorkItem | None: ...

    @abstractmethod
    def update_item(self, item_id: str, payload: WorkItemUpdate) -> WorkItem | None: ...

    @abstractmethod
    def delete_item(self, item_id: str) -> bool: ...


class SQLiteWorkItemRepository(WorkItemRepository):
    def __init__(self, db_path: str | Path):
        self.db_path = Path(db_path)
        self._init_db()

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS work_items (
                    id TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    description TEXT,
                    status TEXT NOT NULL,
                    priority TEXT NOT NULL,
                    assignee TEXT,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                )
                """
            )

    def _row_to_item(self, row: sqlite3.Row) -> WorkItem:
        return WorkItem.model_validate(dict(row))

    def create_item(self, payload: WorkItemCreate) -> WorkItem:
        # TODO: implement in Lab 1.
        raise NotImplementedError("create_item is part of the lab")

    def list_items(self, *, status: WorkStatus | None = None, priority: WorkPriority | None = None) -> list[WorkItem]:
        # TODO: implement in Lab 1.
        raise NotImplementedError("list_items is part of the lab")

    def get_item(self, item_id: str) -> WorkItem | None:
        # TODO: implement in Lab 1.
        raise NotImplementedError("get_item is part of the lab")

    def update_item(self, item_id: str, payload: WorkItemUpdate) -> WorkItem | None:
        # TODO: implement in Lab 1.
        raise NotImplementedError("update_item is part of the lab")

    def delete_item(self, item_id: str) -> bool:
        # TODO: implement in Lab 1.
        raise NotImplementedError("delete_item is part of the lab")
