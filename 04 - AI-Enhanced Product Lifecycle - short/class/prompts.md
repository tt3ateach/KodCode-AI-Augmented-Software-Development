# Module 4 · two-hour class · steps

Copy from here. Chat prompts go to Copilot Chat in **Agent mode**; commands run in the VS Code terminal.
- **New chat:** start a fresh chat (the + button) before that step, so earlier answers don't carry over.
- **Keep:** after an edit you approved, click Keep in the chat before you go on.
- Scroll so the current step is at the top: later steps give answers away.

## Block 1 · Opening

**1.** Run the product, open http://127.0.0.1:8000/ in the browser, then stop it with Ctrl+C:
```
python -m uvicorn app.main:app --port 8000
```

## Block 2 · Requirements

**2.** Prompt:
```
Read inputs/stakeholder_request.md and inputs/messy_backlog.md. List the decisions that are still
missing. Tag each backlog item keep, split, defer or reject, and propose a small first release.
Write one Given/When/Then example. Keep reminder delivery as an open question. Do not edit files.
```

**3.** Slide 5. Load the agreed contract. This command creates `docs/feature_contract.md`; then open that file:
```
python class/go.py contract
```

## Block 3 · Design

**4.** New chat. Prompt:
```
Read docs/feature_contract.md and the code in this workspace (not the class folder). Draw a Mermaid
flowchart of how the due-date feature with an overdue view would fit into this application. Use at most
6 boxes, one per component (not one per file), and mark each NEW or CHANGED. Show where the current date
for the overdue decision comes from. Then list at most three assumptions. Do not edit files.
```

**5.** Prompt, then refresh the browser tab that shows `wireframes.html`:
```
Read docs/feature_contract.md. Overwrite wireframes.html with one self-contained HTML file, grayscale,
no scripts, that shows two low-fidelity wireframes of the Task Tracker side by side. A puts every control
on the task row; B edits dates in a details panel for the selected task. Use the reference day
2026-10-04 and at most four sample tasks that together show every status label. Under each wireframe,
list which REQ each control satisfies. Do not design reminders. Do not edit any other file.
```

## Block 4 · Build and test

**6.** Start the build from a clean stage (this also clears the wireframe page):
```
python class/go.py contract
```
New chat. Prompt:
```
Read docs/feature_contract.md and the baseline code. Plan the smallest due-date change through
validation, SQLite persistence, PATCH field presence, a read-time overdue rule and the existing frontend
modules. List the files you will change and how we will check each one. Wait for approval before editing.
```

**7.** Prompt, after reading the plan. When the edits are done, click Keep:
```
No new dependencies. Leave reminders out. Then go ahead.
```

**8.** Optional prompt, when the edits are done:
```
Review the uncommitted changes in this workspace against docs/feature_contract.md. For each requirement
they touch, say whether the change meets it, and list anything missing or out of scope. Do not edit files.
```

**9.** Run the app, add a date to a task, clear it, then Ctrl+C:
```
python -m uvicorn app.main:app --port 8000
```
If the build went wrong: `python class/go.py built`

**10.** Slide 10. Load the feature with the clearing bug:
```
python class/go.py clearing
```

**11.** Your test, in `tests/test_student_feature.py` (replace the comments):
```python
def test_REQ_03_clear_date_persists_without_losing_title(client):
    created = client.post("/work-items", json={"title": "Review patch", "due_date": "2026-10-03"}).json()
    path = "/work-items/" + created["id"]
    client.patch(path, json={"title": "Review smaller patch"})
    assert client.get(path).json()["due_date"] == "2026-10-03"
    assert client.patch(path, json={"due_date": None}).status_code == 200
    saved = client.get(path).json()
    assert saved["due_date"] is None
    assert saved["title"] == "Review smaller patch"
    assert saved["overdue"] is False
```

**12.** Run it:
```
python -m pytest -q tests/test_student_feature.py
```

**13.** New chat. Prompt:
```
My test in tests/test_student_feature.py checks REQ-03 in docs/feature_contract.md and currently fails.
Explain why it fails, then propose the smallest fix in app/repository.py. Do not change the test.
Afterwards, explain why a title-only PATCH must still keep the date.
```

**14.** Prompt, after reading the proposal. Then click Keep:
```
Go ahead with the fix. Reminder: do not touch the test.
```
If the assistant is slow: `git restore --source 0.4.0 app/repository.py`

**15.** Review and run everything:
```
git diff app/repository.py
python -m pytest -q
```

**16.** Prompt:
```
Expand the acceptance examples in docs/feature_contract.md into at most 8 boundary and combination
cases for the fixed reference day 2026-10-04, as a table: input, expected result, REQ, and whether it is
an API, storage or browser check. Then list eight synthetic tasks around that day as a second table
(name, status, due date) and the exact names Overdue only should return. No code; do not edit files.
```

**17.** Open `class/show/weak_test_example.py`.

## Block 5 · Release

**18.** Load the release that shipped:
```
python class/go.py 0.4.0
```

**19.** New chat. Prompt:
```
Read scripts/verify_release.py, especially semantic_probe(). Name one wrong release this probe would
not catch, and explain why. Answer in four lines or fewer. Do not edit files.
```

**20.** The release rehearsal:
```
python scripts/verify_release.py
```

## Block 6 · Maintenance

**21.** New chat. Prompt:
```
Read only inputs/support_thread.md; don't open any other file. Separate confirmed facts from
hypotheses. Keep the exact task, due date and time. List the plausible explanations and, for each, one
check that would confirm or rule it out. Do not name a cause yet. Do not edit files.
```

**22.** Slide 15. What 0.4.1 changed:
```
git diff 0.4.0 0.4.1 -- app/main.py
```

## Block 7 · Close the loop

**23.** Load release 0.4.1:
```
python class/go.py 0.4.1
```

**24.** New chat. Prompt:
```
Read docs/feature_contract.md (REQ-04) and app/main.py. Propose a pytest test for
tests/test_clock_provider.py that calls the real get_reference_date() with only server_now replaced by
2026-10-04 00:30 at UTC+03:00, and asserts the day REQ-04 requires. Show it and wait for approval.
```

**25.** Prompt, after reading the test with the class. Then click Keep:
```
Go ahead: write it to tests/test_clock_provider.py, replacing the placeholder. Then stop: don't run it
and don't change app code.
```

**26.** Run it:
```
python -m pytest -q tests/test_clock_provider.py
```
If the test didn't get written: `python class/go.py clock-test`

**27.** Prompt:
```
My test in tests/test_clock_provider.py checks REQ-04 in docs/feature_contract.md. Explain its result,
then propose the smallest fix in app/main.py. Do not change the test.
```

**28.** Prompt, after reading the proposal. Then click Keep:
```
Go ahead with the fix. Reminder: do not touch the test.
```
If the assistant is slow: `git restore --source 0.4.2 app/main.py`

**29.** Review and run everything:
```
git diff app/main.py
python -m pytest -q
```

**30.** The mutation check:
```
python class/mutant.py
```

## Block 8 · Fix and handoffs

**31.** Load the fixed release and rehearse it:
```
python class/go.py 0.4.2
python scripts/verify_release.py
```

**32.** New chat. Prompt:
```
Read inputs/fix_0_4_2.diff (the real patch from 0.4.1 to 0.4.2) and tests/test_clock_provider.py. The full
suite passes. Draft a short README note with one example, an internal changelog entry and a user-facing
release note. Include only behavior the patch and tests support. Keep both release texts within 100
words in total. Do not edit files.
```
