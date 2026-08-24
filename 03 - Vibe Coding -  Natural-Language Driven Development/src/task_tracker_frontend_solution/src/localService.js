import { seedTasks } from "./sample-data.js";
import { normalizeTask, updateTask } from "./state.js";

const STORAGE_KEY = "module3-task-tracker";

function loadStoredTasks() {
  try {
    const raw = window.localStorage?.getItem(STORAGE_KEY);
    if (!raw) return [...seedTasks];
    const parsed = JSON.parse(raw);
    return Array.isArray(parsed) ? parsed.map((task, index) => normalizeTask(task, index + 1)) : [...seedTasks];
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
      const task = normalizeTask(input);
      tasks = [task, ...tasks];
      persist(tasks);
      return task;
    },
    async toggleDone(id) {
      const current = tasks.find((task) => task.id === id);
      if (!current) return null;
      const nextStatus = current.status === "done" ? "todo" : "done";
      tasks = updateTask(tasks, id, { status: nextStatus });
      persist(tasks);
      return tasks.find((task) => task.id === id) ?? null;
    },
    async setPriority(id, priority) {
      tasks = updateTask(tasks, id, { priority });
      persist(tasks);
      return tasks.find((task) => task.id === id) ?? null;
    },
    async reset() {
      tasks = [...seedTasks];
      persist(tasks);
      return [...tasks];
    }
  };
}
