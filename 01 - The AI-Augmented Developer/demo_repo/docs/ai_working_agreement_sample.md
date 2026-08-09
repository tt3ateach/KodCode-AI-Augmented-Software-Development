# Sample AI Working Agreement for This Demo Repo

This demo repo uses AI assistance for learning. Keep the workflow intentionally safe:

- Start with read-only explanation.
- Ask for a plan before edits.
- Keep changes small and reviewable.
- Add tests for behavior changes.
- Run `pytest` before accepting changes.
- Do not paste or invent secrets.
- Do not let an agent make broad unrelated changes.

Acceptable demo permissions:

| Permission | Allowed? | Notes |
|---|---|---|
| Read files | Yes | Good first step. |
| Suggest edits | Yes | Review before applying. |
| Edit parser/test files | Yes, for bounded exercises | Keep diff small. |
| Run tests | Yes, after command review | Use `pytest`. |
| Edit unrelated files | No | Ask why it is needed. |
| Commit or push | No, unless instructor explicitly wants to show workflow. |
| Deploy or touch external systems | No | Not part of Module 1. |
