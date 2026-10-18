const STATUS_LABELS = { todo: "Todo", "in-progress": "In progress", done: "Done" };

function clear(element) { element.replaceChildren(); }
function text(tag, className, value) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  node.textContent = value;
  return node;
}

export function renderSummary(container, summary) {
  clear(container);
  for (const [label, value] of [["Total", summary.total], ["Todo", summary.todo], ["In progress", summary["in-progress"]], ["Done", summary.done]]) {
    const card = document.createElement("article");
    card.className = "summary-card";
    card.append(text("div", "summary-label", label), text("div", "summary-value", String(value)));
    container.append(card);
  }
}

function renderTaskCard(task) {
  const card = document.createElement("article");
  card.className = `task-card ${task.status === "done" ? "is-done" : ""}`.trim();
  card.dataset.taskId = task.id;

  const checkbox = document.createElement("input");
  checkbox.className = "checkbox";
  checkbox.type = "checkbox";
  checkbox.checked = task.status === "done";
  checkbox.dataset.action = "toggle-done";
  checkbox.setAttribute("aria-label", `Mark ${task.title} done`);

  const content = document.createElement("div");
  content.append(text("h3", "task-title", task.title));
  content.append(text("div", "task-meta", `Owner: ${task.owner} · Created ${new Date(task.createdAt).toLocaleDateString()}`));

  const badge = text("span", `status-badge ${task.status}`, STATUS_LABELS[task.status] ?? task.status);

  const priority = document.createElement("select");
  priority.className = "priority-select";
  priority.dataset.action = "priority-change";
  priority.setAttribute("aria-label", `Priority for ${task.title}`);
  for (const value of ["low", "medium", "high"]) {
    const option = document.createElement("option");
    option.value = value;
    option.textContent = value[0].toUpperCase() + value.slice(1);
    option.selected = task.priority === value;
    priority.append(option);
  }

  card.append(checkbox, content, badge, priority);
  return card;
}

export function renderTaskList(container, tasks) {
  clear(container);
  if (tasks.length === 0) {
    container.append(text("div", "empty-state", "No tasks match the current filters. Add a task or change the filter."));
    return;
  }
  for (const task of tasks) container.append(renderTaskCard(task));
}
