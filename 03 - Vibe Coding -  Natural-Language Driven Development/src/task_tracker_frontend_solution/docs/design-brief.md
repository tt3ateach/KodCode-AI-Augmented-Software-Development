# Design brief — Task Tracker Frontend

## Product scenario

An engineering team wants a lightweight frontend for tracking work items during a sprint. The Module 2 Work Items API already exists. Module 3 starts with a local-first frontend and then connects the core flow to that API.

## Core user stories

1. As a developer, I can see work items at a glance.
2. As a developer, I can quickly add a new task.
3. As a developer, I can filter tasks by status.
4. As a developer, I can toggle a task between open and done.
5. As a developer, I can update task priority.
6. As a team member, I can keep data locally when the API is not connected.
7. As a team member, I can connect to the Module 2 API for a minimal end-to-end flow.

## Core constraints

- No build tooling.
- No new runtime dependencies.
- Keep the existing file structure understandable.
- Tests cover pure logic and API client behavior.
- DOM behavior is verified manually.
- Do not render user-provided task titles with unsafe `innerHTML`.
- Keep API integration small: list, create, toggle status, update priority, error handling.

## Optional stretch ideas

- free-text search;
- details panel;
- keyboard/focus polish;
- responsive polish;
- dark mode;
- due dates.
