from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import httpx


class WorkItemsClientError(RuntimeError):
    """Raised when the Work Items API returns an error response."""


@dataclass
class WorkItemsClient:
    """Small synchronous client for the classroom Work Items API."""

    base_url: str
    timeout: float = 5.0
    client: httpx.Client | None = None

    def __post_init__(self) -> None:
        self._owns_client = self.client is None
        if self.client is None:
            self.client = httpx.Client(base_url=self.base_url, timeout=self.timeout)

    def close(self) -> None:
        if self._owns_client and self.client is not None:
            self.client.close()

    def _request(self, method: str, path: str, **kwargs: Any) -> Any:
        assert self.client is not None
        response = self.client.request(method, path, **kwargs)
        if response.status_code >= 400:
            raise WorkItemsClientError(f"Work Items API returned {response.status_code}: {response.text}")
        if response.status_code == 204:
            return None
        return response.json()

    def create_work_item(self, title: str, **fields: Any) -> dict[str, Any]:
        payload = {"title": title, **fields}
        return self._request("POST", "/work-items", json=payload)

    def list_work_items(self, *, status: str | None = None, priority: str | None = None) -> list[dict[str, Any]]:
        params = {k: v for k, v in {"status": status, "priority": priority}.items() if v is not None}
        return self._request("GET", "/work-items", params=params)

    def get_work_item(self, item_id: str) -> dict[str, Any]:
        return self._request("GET", f"/work-items/{item_id}")

    def update_work_item(self, item_id: str, **fields: Any) -> dict[str, Any]:
        return self._request("PATCH", f"/work-items/{item_id}", json=fields)

    def delete_work_item(self, item_id: str) -> None:
        return self._request("DELETE", f"/work-items/{item_id}")
