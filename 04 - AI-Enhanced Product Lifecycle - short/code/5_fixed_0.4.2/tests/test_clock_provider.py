"""REQ-04 regression added in 0.4.2.

The older acceptance tests replace get_reference_date with a fixed day, so they never run the real
provider. These tests replace only the clock (server_now) and call the real provider, so they catch a
provider that reads the server's local day instead of the UTC day.
"""

from datetime import date, datetime, timedelta, timezone

from fastapi.testclient import TestClient

import app.main as main
from app.repository import SQLiteWorkItemRepository

UTC_PLUS_3 = timezone(timedelta(hours=3))
# 00:30 on 4 October on a UTC+03:00 server clock is still 21:30 on 3 October in UTC.
LOCAL_AFTER_MIDNIGHT = datetime(2026, 10, 4, 0, 30, tzinfo=UTC_PLUS_3)
# 03:00 at UTC+03:00 is exactly midnight UTC: the UTC day has now advanced too.
UTC_MIDNIGHT = datetime(2026, 10, 4, 3, 0, tzinfo=UTC_PLUS_3)


def test_REQ_04_reference_day_stays_on_utc_day_after_local_midnight(monkeypatch):
    monkeypatch.setattr(main, "server_now", lambda: LOCAL_AFTER_MIDNIGHT)
    assert main.get_reference_date() == date(2026, 10, 3)


def test_REQ_04_reference_day_advances_at_utc_midnight(monkeypatch):
    monkeypatch.setattr(main, "server_now", lambda: UTC_MIDNIGHT)
    assert main.get_reference_date() == date(2026, 10, 4)


def test_REQ_04_api_uses_the_real_provider(tmp_path, monkeypatch):
    repository = SQLiteWorkItemRepository(tmp_path / "clock.db")
    main.app.dependency_overrides[main.get_repository] = lambda: repository
    monkeypatch.setattr(main, "server_now", lambda: LOCAL_AFTER_MIDNIGHT)
    try:
        with TestClient(main.app) as client:
            created = client.post("/work-items", json={"title": "Due 3 October", "due_date": "2026-10-03"})
        assert created.json()["overdue"] is False
    finally:
        main.app.dependency_overrides.clear()
