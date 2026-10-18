from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from app.main import app, get_repository
from app.repository import SQLiteWorkItemRepository


@pytest.fixture
def client(tmp_path):
    repository = SQLiteWorkItemRepository(tmp_path / "test_work_items.db")
    app.dependency_overrides[get_repository] = lambda: repository
    with TestClient(app, raise_server_exceptions=False) as test_client:
        yield test_client
    app.dependency_overrides.clear()
