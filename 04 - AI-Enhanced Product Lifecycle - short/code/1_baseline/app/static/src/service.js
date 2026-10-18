// Preserve the Module 3 service seam. Module 4 uses the live same-origin API.
import { createWorkItemsApiClient } from "./apiClient.js";
export function createTaskService() { return createWorkItemsApiClient(); }
