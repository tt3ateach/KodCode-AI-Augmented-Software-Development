import test from "node:test";
import assert from "node:assert/strict";
import { seedTasks } from "../src/sample-data.js";

test("starter sample data is available for the generated first draft", () => {
  assert.ok(seedTasks.length >= 3);
  for (const task of seedTasks) {
    assert.equal(typeof task.id, "string");
    assert.equal(typeof task.title, "string");
    assert.ok(["todo", "in-progress", "done"].includes(task.status));
  }
});
