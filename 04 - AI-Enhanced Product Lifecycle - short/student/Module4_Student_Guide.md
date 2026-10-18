# Module 4 · The AI-Enhanced Product Lifecycle · Student Guide

Today we follow one small change through the whole lifecycle: optional due dates and an Overdue view in the Work Items product you know from Modules 2 and 3. We go from requirements through design, build, test and release to a bug report after release.

**This file is also your answer sheet.** Write your answers under each *Your answer* heading, and keep your first attempt even if you later use the instructor's example.

| In your package | What it is |
|---|---|
| `Module4_Student_Guide.md` | This guide |
| `inputs/` | The request, backlog, drafts and support evidence the tasks use |
| `code/1_baseline/` | The product before due dates |

Your instructor shares four more files during class, through the course chat:
- the agreed contract, after Task A;
- `2_task_c_start.zip`, the product with the feature built, for Tasks C and D;
- a short thread summary, if you're stuck in Task E;
- `task_f_release_0_4_1.zip`, the 0.4.1 release, for Task F.

---

## Setup (before class)

Use the VS Code, GitHub Copilot and Python setup from Modules 2 and 3. Python 3.12 and 3.13 are tested.

1. **Create the class environment.** Open a terminal in this package folder (the folder that contains this guide), then:
   - **Windows PowerShell:**
     ```powershell
     python -m venv .venv
     .venv\Scripts\Activate.ps1
     python -m pip install -r code/1_baseline/requirements.lock
     ```
     If PowerShell says running scripts is disabled, run `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` once, then activate again.
   - **macOS, Linux or WSL:**
     ```bash
     python3 -m venv .venv
     source .venv/bin/activate
     python -m pip install -r code/1_baseline/requirements.lock
     ```
2. **Check Git.** Run `git --version`. Then run `git config --global user.name`; if it prints nothing, set your name and email once:
   ```bash
   git config --global user.name "Your Name"
   git config --global user.email "you@example.com"
   ```
3. **Check the product.** With the environment active:
   ```bash
   cd code/1_baseline
   python -m pytest -q
   python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
   ```
   Expect `16 passed`. Open http://127.0.0.1:8000/, add a task, complete it, then stop the server with Ctrl+C. If port 8000 is busy, use `--port 8001`.
4. **Point VS Code at the environment.** In class you open a single code folder as your workspace, and VS Code won't find the environment there by itself.
   1. With the environment active, run `python -c "import sys; print(sys.executable)"` and copy the path it prints.
   2. Open `code/1_baseline/` in VS Code, run **Python: Select Interpreter** from the Command Palette, choose **Enter interpreter path…**, and paste the path.
   3. Do the same each time you open another code folder in class.

   If a new VS Code terminal doesn't show `(.venv)` in its prompt, activate the environment there: `..\..\.venv\Scripts\Activate.ps1` on Windows, `source ../../.venv/bin/activate` on macOS, Linux or WSL.

If setup fails in class, don't spend the session on it: follow the instructor's screen and note that you reviewed instead of ran.

---

## How the class works

- **Each block:** the instructor demos with the assistant, then pairs do a smaller version of the same thing, then the instructor shows a worked answer.
- **Stop times are stop times.** A partial answer is fine.
- **Pairs:** one person drives the assistant and the keyboard; the other checks every result against the task's minimum and, from Task C on, against the contract. Swap at each task.
- **Follow along:** during demos you may run the same prompt in your own copy. Nothing is collected.
- **If a reply takes more than about 60 seconds,** stop waiting and follow the instructor's screen.
- **Across the whole class,** keep a note of one AI suggestion you rejected or revised (there's a space at the end).
- **Don't open `inputs/maintenance/` before Task E.** It's the evidence for a later task.

**Never open this whole package folder as your VS Code workspace.** Open only the folder a task names, so the assistant reads only what it should.

| Task | Open as your workspace | Copilot mode | Also give the assistant |
|---|---|---|---|
| A | `code/1_baseline/` | Ask | `inputs/stakeholder_request.md` and `inputs/messy_backlog.md`: drag both files from your file manager into the chat box, or paste their text. (VS Code's file picker lists only workspace files.) |
| B | `code/1_baseline/` | Ask | — |
| C | `code/2_task_c_start/` (from the Task C zip) | Agent | — |
| D | `code/2_task_c_start/` | Ask | — |
| E | `inputs/maintenance/` | Ask | — (so the assistant answers from the evidence, not the code) |
| F | `code/task_f_release_0_4_1/` (from the Task F zip) | Agent | — |

### Unzipping a class zip

Each zip contains one folder. It must end up directly inside your `code/` folder, next to `1_baseline/`, so that the environment is two folders up.
- **Windows:** right-click the zip, choose **Extract All**, and set the destination to your package's `code` folder. Delete the extra folder name Windows adds at the end of the path (for example `\2_task_c_start`).
- **macOS:** double-clicking extracts the folder next to the zip, usually in Downloads. Move the extracted folder into `code/`.
- **Linux or WSL:** with the environment active, from the package folder, run `python -m zipfile -e ~/Downloads/2_task_c_start.zip code/` (use the zip's own name; under WSL, your Windows downloads are in `/mnt/c/Users/<you>/Downloads/`).

Then check that the folder's `README.md` sits directly inside it, for example `code/2_task_c_start/README.md`.

---

## Task A · Requirements · 10 minutes

**Minimum:** one Given/When/Then example, one open decision, one deferred backlog item.

```text
Read the attached stakeholder request and draft backlog. List the decisions that are still missing.
Tag each backlog item keep, split, defer or reject, and propose a small first release.
Write one Given/When/Then example. Keep reminder delivery as an open question. Do not edit code.
```

### Your answer

*Replace this line.*

---

## Task B · Design · 5 minutes

**Minimum:** one wrong, missing or invented part in the AI's architecture diagram, and why it matters. If your diagram looks correct, critique `inputs/prepared_architecture_draft.mmd` instead.

```text
Read the code in this workspace. Draw a Mermaid flowchart of how a due-date feature with an overdue view
would fit into this application. Use at most 6 boxes, one per component (not one per file), and mark each
NEW or CHANGED. Show where the current date for the overdue decision comes from. Then list at most three
assumptions. Do not edit files.
```

Don't read the diagram line by line. Ask four questions of it: which components change, what's new, where "today" comes from, and what a cleared date passes through. A question the diagram can't answer is a finding too. If the chat shows Mermaid text instead of a drawing, read the text; at six boxes it's short.

### Your answer

*Replace this line.*

---

## Task C · Build and test · 15 minutes

**Minimum:** your own failing test for the clearing rule, the smallest fix, and the full-suite result.

Unzip the Task C zip your instructor shares (see *Unzipping a class zip*), open `code/2_task_c_start/` as your workspace, select the interpreter as in Setup step 4, and follow its `README.md`. The README has the steps and the fix prompt; the contract is in its `docs/` folder.

### Your answer

*Replace this line.*

---

## Task D · Release · 5 minutes

**Minimum:** one wrong release the business probe (`semantic_probe()`) would not catch, and why.

Stay in `code/2_task_c_start/`.

```text
Read scripts/verify_release.py, especially semantic_probe(). Name one wrong release this probe would not
catch, and explain why. Answer in four lines or fewer.
```

Keep your answer: the class comes back to it in the next block.

### Your answer

*Replace this line.*

---

## Task E · Maintenance · 10 minutes

**Minimum:** two facts with their times, one hypothesis, and one check that would tell the hypotheses apart.

Open `inputs/maintenance/` as your workspace.

```text
Summarize the support thread, request log and release record in this folder. Separate confirmed facts, each
with its UTC time, from hypotheses. Keep the exact task, due date and times. List the plausible
explanations and, for each, one check that would confirm or rule it out. Do not name a cause yet.
```

### Your answer

*Replace this line.*

---

## Task F · Close the loop · 25 minutes (four-hour class)

**Minimum:** a test that fails on 0.4.1, the fix, one mutation result, and an answer to the question: why did the 34 shipped tests pass?

Unzip the Task F zip as in Task C, open `code/task_f_release_0_4_1/` as your workspace, select the interpreter, and follow its `README.md`.

### Your answer

*Replace this line.*

---

## Exit question · 5 minutes

Pick one requirement. Where could a mistake be caught, and which checks might still miss it? Name a concrete wrong result, one check that would catch it, and one that would miss it.

### Your answer

*Replace this line, or answer aloud.*

## One AI suggestion we rejected or revised

What did the assistant suggest, what did you change, and why?

### Your answer

*Replace this line.*

---

## Optional homework (after class)

1. **Task F**, if your class ran three hours: ask your instructor for the 0.4.1 release zip and follow its README.
2. **Reminder discovery:** ask the assistant which questions must be answered before reminders can be built, and turn them into a short discovery backlog. Keep reminders separate from due dates.
3. **Business timezone:** write a one-page proposal on which timezone should define "today" for a team that works in local time. Say what would change in the contract, the code and the tests, including around a daylight-saving change.
4. **Role handoff:** take a different small feature and show what product, development, QA, operations and support each hand to the next person, using requirement IDs.

---

## Glossary

| Term | Meaning in this class |
|---|---|
| Calendar date | A day such as `2026-10-04`, with no time of day |
| Reference day | The day the API treats as "today" when it decides whether a task is overdue |
| Clock seam | A single place where the code asks for the current time, so a test can replace it with a fixed moment |
| Acceptance example | A concrete input and the result the stakeholder agreed should happen, often written Given/When/Then |
| Spec-driven development | Write the agreed behavior down first (the spec), plan against it, then implement. Our contract is the spec. |
| Repository instructions | A file such as `AGENTS.md` that the assistant reads for project rules |
| Liveness check | `/health` answers whether the process responds |
| Business probe | Exercises one product rule against the running app |
| Discriminating check | A check whose result helps you choose between competing explanations |
| Test double | A stand-in for a real component, used in a test to make the result predictable |
| Mutation | A deliberate wrong change to the code, used to see whether the tests notice |
| Ask mode, Agent mode | Copilot Chat modes: Ask answers in the chat; Agent can also edit files and run commands in your workspace |
