# Module 3 Setup Guide — Vibe Coding and Natural-Language-Driven Development

**Course:** AI-Augmented Software Development  
**Module:** 3  
**Version:** v1  
**Classroom baseline:** GitHub Copilot in VS Code, with optional comparison to Claude Code, Codex, Continue, or OpenHands.

## Module continuity

Module 2 taught a disciplined AI-assisted development loop:

> Frame → Plan → Prompt → Execute → Verify → Reflect

Module 3 does **not** replace that workflow. It stress-tests it. In this module, students start closer to product intent and let AI generate a larger first draft. Because the first draft is faster and broader, the need for containment, verification, and ownership increases.

## Required local tools

- Node.js 22 LTS or compatible recent Node version. The package was validated with Node `v22.16.0`.
- npm 10+.
- A static file server. The repos include an npm script using Python’s `http.server`, so Python 3.11+ is convenient but not required for the frontend tests.
- Git.
- VS Code or another IDE with the chosen AI coding assistant.
- Optional for end-to-end integration: the Module 2 Work Items API solution running at `http://127.0.0.1:8000`.

## Student setup

```bash
cd task_tracker_frontend_starter
npm install
npm test
npm run serve
```

Open:

```text
http://127.0.0.1:8000
```

The starter repo is intentionally incomplete. Some acceptance tests fail until students build the core frontend behavior.

## Instructor setup checklist

Before class:

1. Open `module3_slides.pptx` and confirm speaker notes are visible.
2. Open `module3_companion_notebook.ipynb`.
3. Open `task_tracker_frontend_starter/` in the IDE.
4. Confirm the student environment can run `npm test`.
5. Confirm the solution environment can run `npm test`.
6. Optional: start the Module 2 API solution if you want to demonstrate the end-to-end integration live.
7. Keep `module3_demo_runbook.md` open during demos.

## Optional API integration setup

From the synced Module 2 package:

```bash
cd work_items_api_solution
python -m venv .venv
source .venv/bin/activate      # Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Then in the Module 3 frontend solution, set the API base URL in the app UI:

```text
http://127.0.0.1:8000
```

The integration is intentionally small: list, create, status toggle, priority update, and error handling. There is no authentication in this classroom exercise.

## Optional topics for pacing

Clearly marked optional content may be skipped or skimmed when a cohort needs more lab time:

- detailed tool comparison among Copilot, Claude Code, Codex, Continue, and OpenHands;
- local/self-hosted vibe-coding environments;
- screenshot-to-code and visual asset generation;
- UI polish beyond the core behavior;
- dark mode, detail panels, rich filtering, or other stretch UI ideas.

Do **not** skip:

- the Module 2 → Module 3 continuity frame;
- the definition of vibe coding;
- Brief → Generate/Contain → Review → Own;
- risk and fit discussion;
- the AI handoff problem;
- Phase 2 ownership work;
- the minimal Module 2 API integration.

## Fallbacks

If live AI access fails:

1. Use the prepared prompts and expected outputs in `module3_demo_runbook.md`.
2. Use `task_tracker_frontend_solution/` as the fallback final state.
3. Use `review_exercises/flawed_generated_draft/` to teach ownership and critique without live generation.
4. Continue the class using the notebook solutions.
