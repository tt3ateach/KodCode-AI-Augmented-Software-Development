import test from "node:test";
import assert from "node:assert/strict";
import { normalizeTask, applyFilters, updateTask, summarizeTasks, toApiStatus, fromApiStatus, mapApiWorkItem, toApiCreatePayload } from "../src/state.js";

test("normalizeTask trims title and fills defaults", () => {
  const task = normalizeTask({ title: "  Write docs  ", priority: "high" }, 999);
  assert.equal(task.id, "local-999");
  assert.equal(task.title, "Write docs");
  assert.equal(task.status, "todo");
  assert.equal(task.priority, "high");
});

test("normalizeTask rejects empty titles", () => {
  assert.throws(() => normalizeTask({ title: "   " }), /required/i);
});

test("applyFilters filters by status and search and sorts newest first", () => {
  const tasks = [
    { id: "1", title: "Write docs", status: "todo", priority: "low", createdAt: "2026-07-01T10:00:00.000Z" },
    { id: "2", title: "Fix navbar", status: "done", priority: "medium", createdAt: "2026-07-02T10:00:00.000Z" },
    { id: "3", title: "Write tests", status: "todo", priority: "high", createdAt: "2026-07-03T10:00:00.000Z" }
  ];
  const visible = applyFilters(tasks, { status: "todo", search: "write" });
  assert.deepEqual(visible.map((task) => task.id), ["3", "1"]);
});

test("updateTask patches only the matching task and preserves invalid status values", () => {
  const tasks = [{ id: "1", title: "A", status: "todo", priority: "low" }, { id: "2", title: "B", status: "done", priority: "medium" }];
  const updated = updateTask(tasks, "1", { status: "nope", priority: "high" });
  assert.equal(updated[0].status, "todo");
  assert.equal(updated[0].priority, "high");
  assert.equal(updated[1].priority, "medium");
});

test("summarizeTasks counts each status", () => {
  assert.deepEqual(summarizeTasks([{ status: "todo" }, { status: "in-progress" }, { status: "done" }]), { total: 3, todo: 1, "in-progress": 1, done: 1 });
});

test("API status mapping converts between frontend and Module 2 API naming", () => {
  assert.equal(toApiStatus("in-progress"), "in_progress");
  assert.equal(fromApiStatus("in_progress"), "in-progress");
});

test("mapApiWorkItem converts a Module 2 API item into a frontend task", () => {
  const task = mapApiWorkItem({ id: "42", title: "API task", status: "in_progress", priority: "high", assignee: "Ari", created_at: "2026-07-01T10:00:00", updated_at: "2026-07-02T10:00:00" });
  assert.equal(task.id, "42");
  assert.equal(task.status, "in-progress");
  assert.equal(task.owner, "Ari");
  assert.equal(task.createdAt, "2026-07-01T10:00:00");
});

test("toApiCreatePayload sends only the fields the API expects", () => {
  assert.deepEqual(toApiCreatePayload({ title: "New", priority: "high", owner: "Dana" }), { title: "New", description: null, priority: "high", status: "todo", assignee: "Dana" });
});
