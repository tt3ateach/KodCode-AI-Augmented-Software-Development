import { mapApiWorkItem, toApiCreatePayload, toApiStatus } from "./state.js";

async function parseJsonOrThrow(response) {
  if (!response.ok) throw new Error(`API request failed with status ${response.status}`);
  if (response.status === 204) return null;
  return response.json();
}

function jsonRequest(method, body) {
  return { method, headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) };
}

export function createWorkItemsApiClient(baseUrl, fetchImpl = fetch) {
  const root = baseUrl.replace(/\/$/, "");
  return {
    async list() {
      const data = await parseJsonOrThrow(await fetchImpl(`${root}/work-items`));
      return data.map(mapApiWorkItem);
    },
    async create(input) {
      const data = await parseJsonOrThrow(await fetchImpl(`${root}/work-items`, jsonRequest("POST", toApiCreatePayload(input))));
      return mapApiWorkItem(data);
    },
    async updateStatus(id, status) {
      const data = await parseJsonOrThrow(await fetchImpl(`${root}/work-items/${encodeURIComponent(id)}`, jsonRequest("PATCH", { status: toApiStatus(status) })));
      return mapApiWorkItem(data);
    },
    async updatePriority(id, priority) {
      const data = await parseJsonOrThrow(await fetchImpl(`${root}/work-items/${encodeURIComponent(id)}`, jsonRequest("PATCH", { priority })));
      return mapApiWorkItem(data);
    }
  };
}
