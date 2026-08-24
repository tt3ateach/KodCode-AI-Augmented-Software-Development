import { seedTasks } from "./sample-data.js";
import { normalizeTask, updateTask } from "./state.js";

const STORAGE_KEY = "module3-task-tracker";

function loadStoredTasks() {
  try {
    const raw = window.localStorage?.getItem(STORAGE_KEY);
    if (!raw) return [...seedTasks];
    const parsed = JSON.parse(raw);
    return Array.isArray(parsed) ? parsed : [...seedTasks];
  } catch {
    return [...seedTasks];
  }
}

function persist(tasks) {
  window.localStorage?.setItem(STORAGE_KEY, JSON.stringify(tasks));
}

export function createLocalTaskService() {
  let tasks = loadStoredTasks();
  return {
    async list() { return [...tasks]; },
    async create(input) {
      // TODO: normalize, prepend, persist, and return the task.
      throw new Error("Not implemented yet.");
    },
    async toggleDone(id) {
      // TODO: toggle status between todo and done.
      throw new Error("Not implemented yet.");
    },
    async setPriority(id, priority) {
      // TODO: set valid priority and persist.
      throw new Error("Not implemented yet.");
    },
    async reset() {
      tasks = [...seedTasks];
      persist(tasks);
      return [...tasks];
    }
  };
}
