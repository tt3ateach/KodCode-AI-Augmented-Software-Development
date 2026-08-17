from __future__ import annotations

import httpx
import pytest

from app.client import WorkItemsClient, WorkItemsClientError


def make_client(handler):
    transport = httpx.MockTransport(handler)
    httpx_client = httpx.Client(transport=transport, base_url="http://testserver")
    return WorkItemsClient(base_url="http://testserver", client=httpx_client)


def test_create_work_item_uses_timeout_ready_httpx_client_shape():
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.method == "POST"
        assert request.url.path == "/work-items"
        assert request.read() == b'{"title":"Write docs","priority":"high"}'
        return httpx.Response(201, json={"id": "item-1", "title": "Write docs"})

    client = make_client(handler)

    assert client.create_work_item("Write docs", priority="high") == {"id": "item-1", "title": "Write docs"}


def test_list_work_items_passes_filters():
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/work-items"
        assert request.url.params["status"] == "todo"
        assert request.url.params["priority"] == "high"
        return httpx.Response(200, json=[])

    client = make_client(handler)

    assert client.list_work_items(status="todo", priority="high") == []


def test_delete_work_item_handles_204_response():
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.method == "DELETE"
        assert request.url.path == "/work-items/item-1"
        return httpx.Response(204)

    client = make_client(handler)

    assert client.delete_work_item("item-1") is None


def test_client_raises_clear_error_for_http_failures():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(404, text="not found")

    client = make_client(handler)

    with pytest.raises(WorkItemsClientError, match="404"):
        client.get_work_item("missing")
