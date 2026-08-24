import { mapApiWorkItem, toApiCreatePayload, toApiStatus } from "./state.js";

async function parseJsonOrThrow(response) {
  if (!response.ok) throw new Error(`API request failed with status ${response.status}`);
  if (response.status === 204) return null;
  return response.json();
}

export function createWorkItemsApiClient(baseUrl, fetchImpl = fetch) {
  const root = baseUrl.replace(/\/$/, "");
  return {
    async list() {
      // TODO: GET /work-items and map API items to frontend tasks.
      throw new Error("Not implemented yet.");
    },
    async create(input) {
      // TODO: POST /work-items.
      throw new Error("Not implemented yet.");
    },
    async updateStatus(id, status) {
      // TODO: PATCH /work-items/{id} with API status.
      throw new Error("Not implemented yet.");
    },
    async updatePriority(id, priority) {
      // TODO: PATCH /work-items/{id}.
      throw new Error("Not implemented yet.");
    }
  };
}
