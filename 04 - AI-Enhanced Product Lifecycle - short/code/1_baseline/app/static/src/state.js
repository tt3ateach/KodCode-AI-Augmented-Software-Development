export const DEFAULT_FILTERS = { status: "all", search: "" };
export const ALLOWED_STATUS = new Set(["todo", "in-progress", "done"]);
export const ALLOWED_PRIORITY = new Set(["low", "medium", "high"]);

export function normalizeTask(input, nextId = Date.now()) {
  const title = (input?.title ?? "").trim();
  if (!title) throw new Error("Task title is required.");
  const now = new Date().toISOString();
  return {
    id: input?.id ?? `local-${nextId}`,
    title,
    status: ALLOWED_STATUS.has(input?.status) ? input.status : "todo",
    priority: ALLOWED_PRIORITY.has(input?.priority) ? input.priority : "medium",
    owner: (input?.owner ?? "Unassigned").trim() || "Unassigned",
    createdAt: input?.createdAt ?? now,
    updatedAt: input?.updatedAt ?? input?.createdAt ?? now
  };
}

export function applyFilters(tasks, filters = DEFAULT_FILTERS) {
  const status = filters?.status ?? "all";
  const searchTerm = (filters?.search ?? "").trim().toLowerCase();
  return [...tasks]
    .filter((task) => status === "all" || task.status === status)
    .filter((task) => {
      if (!searchTerm) return true;
      return [task.title, task.owner, task.priority, task.status].some((value) => String(value ?? "").toLowerCase().includes(searchTerm));
    })
    .sort((left, right) => new Date(right.createdAt).getTime() - new Date(left.createdAt).getTime());
}

export function updateTask(tasks, id, patch) {
  const now = new Date().toISOString();
  return tasks.map((task) => {
    if (task.id !== id) return task;
    const nextStatus = ALLOWED_STATUS.has(patch?.status) ? patch.status : task.status;
    const nextPriority = ALLOWED_PRIORITY.has(patch?.priority) ? patch.priority : task.priority;
    return { ...task, ...patch, status: nextStatus, priority: nextPriority, updatedAt: now };
  });
}

export function summarizeTasks(tasks) {
  const summary = { total: tasks.length, todo: 0, "in-progress": 0, done: 0 };
  for (const task of tasks) {
    if (summary[task.status] !== undefined) summary[task.status] += 1;
  }
  return summary;
}

export function toApiStatus(status) {
  return status === "in-progress" ? "in_progress" : status;
}

export function fromApiStatus(status) {
  return status === "in_progress" ? "in-progress" : status;
}

export function mapApiWorkItem(item) {
  return normalizeTask({
    id: String(item.id),
    title: item.title,
    status: fromApiStatus(item.status),
    priority: item.priority,
    owner: item.assignee ?? "Unassigned",
    createdAt: item.created_at ?? item.createdAt,
    updatedAt: item.updated_at ?? item.updatedAt ?? item.created_at
  });
}

export function toApiCreatePayload(input) {
  return {
    title: (input?.title ?? "").trim(),
    description: input?.description ?? null,
    status: toApiStatus(input?.status ?? "todo"),
    priority: ALLOWED_PRIORITY.has(input?.priority) ? input.priority : "medium",
    assignee: input?.owner ?? input?.assignee ?? "Unassigned"
  };
}
