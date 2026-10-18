import { mapApiWorkItem, toApiCreatePayload, toApiStatus } from "./state.js";

export function createWorkItemsApiClient(baseUrl = "", fetchImpl = fetch) {
  const root = baseUrl.replace(/\/$/, "");
  async function request(path, method = "GET", body) {
    const options = { method };
    if (body !== undefined) {
      options.headers = { "Content-Type": "application/json" };
      options.body = JSON.stringify(body);
    }
    const response = await fetchImpl(root + path, options);
    if (!response.ok) throw new Error(`API request failed with status ${response.status}`);
    return response.status === 204 ? null : response.json();
  }
  const itemPath = id => `/work-items/${encodeURIComponent(id)}`;
  const patch = async (id, body) => mapApiWorkItem(await request(itemPath(id), "PATCH", body));
  return {
    async list() { return (await request("/work-items")).map(mapApiWorkItem); },
    async create(input) { return mapApiWorkItem(await request("/work-items", "POST", toApiCreatePayload(input))); },
    async toggleDone(id) {
      const current = await request(itemPath(id));
      return patch(id, { status: current.status === "done" ? "todo" : "done" });
    },
    async setPriority(id, priority) { return patch(id, { priority }); },
    async updateStatus(id, status) { return patch(id, { status: toApiStatus(status) }); },

  };
}
