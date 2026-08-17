from __future__ import annotations

import sqlite3
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

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
        now = utc_now()
        item = WorkItem(
            id=new_work_item_id(),
            title=payload.title,
            description=payload.description,
            status=payload.status,
            priority=payload.priority,
            assignee=payload.assignee,
            created_at=now,
            updated_at=now,
        )
        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO work_items (id, title, description, status, priority, assignee, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    item.id,
                    item.title,
                    item.description,
                    item.status.value,
                    item.priority.value,
                    item.assignee,
                    item.created_at.isoformat(),
                    item.updated_at.isoformat(),
                ),
            )
        return item

    def list_items(self, *, status: WorkStatus | None = None, priority: WorkPriority | None = None) -> list[WorkItem]:
        query = "SELECT * FROM work_items"
        clauses: list[str] = []
        params: list[Any] = []
        if status is not None:
            clauses.append("status = ?")
            params.append(status.value)
        if priority is not None:
            clauses.append("priority = ?")
            params.append(priority.value)
        if clauses:
            query += " WHERE " + " AND ".join(clauses)
        query += " ORDER BY created_at ASC, id ASC"
        with self._connect() as conn:
            rows = conn.execute(query, params).fetchall()
        return [self._row_to_item(row) for row in rows]

    def get_item(self, item_id: str) -> WorkItem | None:
        with self._connect() as conn:
            row = conn.execute("SELECT * FROM work_items WHERE id = ?", (item_id,)).fetchone()
        return self._row_to_item(row) if row is not None else None

    def update_item(self, item_id: str, payload: WorkItemUpdate) -> WorkItem | None:
        existing = self.get_item(item_id)
        if existing is None:
            return None
        update_data = payload.model_dump(exclude_unset=True)
        values = existing.model_dump()
        values.update(update_data)
        values["updated_at"] = utc_now()
        updated = WorkItem.model_validate(values)
        with self._connect() as conn:
            conn.execute(
                """
                UPDATE work_items
                SET title = ?, description = ?, status = ?, priority = ?, assignee = ?, updated_at = ?
                WHERE id = ?
                """,
                (
                    updated.title,
                    updated.description,
                    updated.status.value,
                    updated.priority.value,
                    updated.assignee,
                    updated.updated_at.isoformat(),
                    updated.id,
                ),
            )
        return updated

    def delete_item(self, item_id: str) -> bool:
        with self._connect() as conn:
            cursor = conn.execute("DELETE FROM work_items WHERE id = ?", (item_id,))
        return cursor.rowcount == 1
