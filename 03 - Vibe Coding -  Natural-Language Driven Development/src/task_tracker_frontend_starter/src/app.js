import { createTaskService } from "./service.js";
import { DEFAULT_FILTERS, applyFilters, summarizeTasks } from "./state.js";
import { renderSummary, renderTaskList } from "./render.js";

let service = createTaskService();
const filters = { ...DEFAULT_FILTERS };

const elements = {
  summary: document.querySelector("#summary"),
  taskList: document.querySelector("#task-list"),
  flash: document.querySelector("#flash-message"),
  quickAddForm: document.querySelector("#quick-add-form"),
  titleInput: document.querySelector("#task-title-input"),
  priorityInput: document.querySelector("#task-priority-input"),
  searchInput: document.querySelector("#search-input"),
  filterChips: [...document.querySelectorAll(".filter-chip")],
  apiUrlInput: document.querySelector("#api-url-input"),
  connectApiButton: document.querySelector("#connect-api-button"),
  useLocalButton: document.querySelector("#use-local-button"),
  modeLabel: document.querySelector("#mode-label")
};

function setFlashMessage(message) { elements.flash.textContent = message; }
function syncFilterUi() {
  elements.filterChips.forEach((chip) => chip.classList.toggle("is-active", chip.dataset.status === filters.status));
}
async function refresh() {
  const tasks = await service.list();
  const visibleTasks = applyFilters(tasks, filters);
  renderSummary(elements.summary, summarizeTasks(tasks));
  renderTaskList(elements.taskList, visibleTasks);
  syncFilterUi();
}

elements.quickAddForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  // TODO: create task, clear input, refresh.
});

elements.searchInput.addEventListener("input", async (event) => {
  filters.search = event.target.value;
  await refresh();
});

for (const chip of elements.filterChips) {
  chip.addEventListener("click", async () => { filters.status = chip.dataset.status; await refresh(); });
}

elements.taskList.addEventListener("change", async (event) => {
  // TODO: handle toggle and priority changes.
});

elements.connectApiButton.addEventListener("click", async () => {
  // TODO: switch to API mode and handle connection errors.
});

elements.useLocalButton.addEventListener("click", async () => {
  service = createTaskService();
  elements.modeLabel.textContent = "Local mode";
  await refresh();
});

refresh();
