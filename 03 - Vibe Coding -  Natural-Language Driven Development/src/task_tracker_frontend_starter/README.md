# Task Tracker Frontend — Minimal Starter

This starter supports Module 3: vibe coding and natural-language-driven development.

It is intentionally **under-designed**. The product intent, constraints, and sample data are present, but the application architecture and implementation are not.

That is deliberate: the coding agent should first help propose the product slice and file responsibilities rather than merely fill predefined TODOs.

## Start here

1. Read `docs/design-brief.md`.
2. Run the starter test:

```bash
npm install
npm test
```

3. Serve the current shell:

```bash
npm run serve
```

4. Use the Module 3 prompt progression:
   - explore product intent;
   - contain the first slice;
   - generate the first draft;
   - verify and review;
   - take ownership;
   - then integrate the Module 2 API.

## Expected starting state

- `npm test` passes a small sanity check for the supplied sample data.
- The browser shows only a minimal shell.
- There is **no predefined application architecture** to complete.
- The coding agent is expected to propose and create the implementation files after the plan is reviewed.

## Phase 1 target behavior

The first local-only slice should eventually support:

- rendering tasks;
- quick-add;
- one status filter;
- toggling completion;
- local persistence;
- an empty state.

Search, priority editing, visual polish, and richer controls are optional stretch work.

## Phase 2

After the first draft is working and reviewed, connect the core flow to the Module 2 Work Items API while keeping local mode available as fallback.
