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
  filterChips: [...document.querySelectorAll(".filter-chip")]

};

function setFlashMessage(message, isError = false) {
  elements.flash.textContent = message;
  elements.flash.style.color = isError ? "var(--danger)" : "var(--accent-2)";
}

function syncFilterUi() {
  elements.filterChips.forEach((chip) => chip.classList.toggle("is-active", chip.dataset.status === filters.status));
}

async function refresh() {
  try {
    const tasks = await service.list();
    const visibleTasks = applyFilters(tasks, filters);
    renderSummary(elements.summary, summarizeTasks(tasks));
    renderTaskList(elements.taskList, visibleTasks);
    syncFilterUi();
  } catch (error) {
    setFlashMessage(error.message || "Could not refresh tasks.", true);
  }
}

elements.quickAddForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  try {
    await service.create({ title: elements.titleInput.value, priority: elements.priorityInput.value });
    elements.titleInput.value = "";
    setFlashMessage("Task added.");
    await refresh();
  } catch (error) {
    setFlashMessage(error.message || "Could not add task.", true);
  }
});

elements.searchInput.addEventListener("input", async (event) => {
  filters.search = event.target.value;
  await refresh();
});

for (const chip of elements.filterChips) {
  chip.addEventListener("click", async () => { filters.status = chip.dataset.status; await refresh(); });
}

elements.taskList.addEventListener("change", async (event) => {
  const card = event.target.closest("[data-task-id]");
  if (!card) return;
  try {
    if (event.target.dataset.action === "toggle-done") {
      await service.toggleDone(card.dataset.taskId);
      setFlashMessage("Updated task status.");
    }
    if (event.target.dataset.action === "priority-change") {
      await service.setPriority(card.dataset.taskId, event.target.value);
      setFlashMessage("Updated priority.");
    }
    await refresh();
  } catch (error) {
    setFlashMessage(error.message || "Could not update task.", true);
  }
});

refresh();
