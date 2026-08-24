import { createLocalTaskService } from "./localService.js";
import { createWorkItemsApiClient } from "./apiClient.js";

export function createTaskService({ mode = "local", apiBaseUrl = "" } = {}) {
  if (mode === "api" && apiBaseUrl) {
    return createWorkItemsApiClient(apiBaseUrl);
  }
  return createLocalTaskService();
}
