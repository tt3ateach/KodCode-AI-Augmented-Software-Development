const STATUS_LABELS = { todo: "Todo", "in-progress": "In progress", done: "Done" };

function clear(element) { element.replaceChildren(); }

export function renderSummary(container, summary) {
  clear(container);
  for (const [label, value] of [["Total", summary.total], ["Todo", summary.todo], ["In progress", summary["in-progress"]], ["Done", summary.done]]) {
    const card = document.createElement("article");
    card.className = "summary-card";
    card.innerHTML = `<div class="summary-label"></div><div class="summary-value"></div>`;
    card.querySelector(".summary-label").textContent = label;
    card.querySelector(".summary-value").textContent = value;
    container.append(card);
  }
}

export function renderTaskList(container, tasks) {
  // TODO: render empty state and task cards using safe DOM node creation.
  clear(container);
}
