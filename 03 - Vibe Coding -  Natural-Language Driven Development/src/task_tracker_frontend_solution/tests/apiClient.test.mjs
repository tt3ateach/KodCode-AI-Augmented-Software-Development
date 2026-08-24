import test from "node:test";
import assert from "node:assert/strict";
import { createWorkItemsApiClient } from "../src/apiClient.js";

function fakeResponse(body, init = {}) {
  return { ok: init.ok ?? true, status: init.status ?? 200, async json() { return body; } };
}

test("API client lists and maps work items", async () => {
  const calls = [];
  const client = createWorkItemsApiClient("http://api.test", async (url, options) => {
    calls.push({ url, options });
    return fakeResponse([{ id: "1", title: "From API", status: "in_progress", priority: "medium", assignee: "Dana", created_at: "now", updated_at: "now" }]);
  });
  const tasks = await client.list();
  assert.equal(calls[0].url, "http://api.test/work-items");
  assert.equal(tasks[0].status, "in-progress");
});

test("API client sends create payload as JSON", async () => {
  const calls = [];
  const client = createWorkItemsApiClient("http://api.test/", async (url, options) => {
    calls.push({ url, options });
    return fakeResponse({ id: "2", title: "New", status: "todo", priority: "high", assignee: "Ari", created_at: "now", updated_at: "now" });
  });
  const task = await client.create({ title: "New", priority: "high", owner: "Ari" });
  assert.equal(calls[0].url, "http://api.test/work-items");
  assert.equal(calls[0].options.method, "POST");
  assert.equal(JSON.parse(calls[0].options.body).assignee, "Ari");
  assert.equal(task.id, "2");
});

test("API client surfaces non-OK responses", async () => {
  const client = createWorkItemsApiClient("http://api.test", async () => fakeResponse({ detail: "bad" }, { ok: false, status: 500 }));
  await assert.rejects(() => client.list(), /500/);
});
