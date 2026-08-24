export const DEFAULT_FILTERS = { status: "all", search: "" };
export const ALLOWED_STATUS = new Set(["todo", "in-progress", "done"]);
export const ALLOWED_PRIORITY = new Set(["low", "medium", "high"]);

export function normalizeTask(input, nextId = Date.now()) {
  const title = (input?.title ?? "").trim();
  if (!title) throw new Error("Task title is required.");
  return {
    id: input?.id ?? `local-${nextId}`,
    title,
    status: ALLOWED_STATUS.has(input?.status) ? input.status : "todo",
    priority: ALLOWED_PRIORITY.has(input?.priority) ? input.priority : "medium",
    owner: (input?.owner ?? "Unassigned").trim() || "Unassigned",
    createdAt: input?.createdAt ?? new Date().toISOString(),
    updatedAt: input?.updatedAt ?? new Date().toISOString()
  };
}

export function applyFilters(tasks, filters = DEFAULT_FILTERS) {
  // TODO: support status filtering, optional search, and deterministic newest-first ordering.
  return [...tasks];
}

export function updateTask(tasks, id, patch) {
  // TODO: update only the matching task while preserving invalid status/priority values.
  return tasks;
}

export function summarizeTasks(tasks) {
  // TODO: return { total, todo, "in-progress", done }.
  return { total: tasks.length, todo: 0, "in-progress": 0, done: 0 };
}

export function toApiStatus(status) {
  return status === "in-progress" ? "in_progress" : status;
}

export function fromApiStatus(status) {
  return status === "in_progress" ? "in-progress" : status;
}

export function mapApiWorkItem(item) {
  // TODO: map Module 2 API fields to frontend task shape.
  return item;
}

export function toApiCreatePayload(input) {
  // TODO: map frontend quick-add input to Module 2 API payload.
  return input;
}
