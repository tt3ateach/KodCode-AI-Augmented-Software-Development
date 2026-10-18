# Module 4 · The AI-Enhanced Product Lifecycle · Two-hour version · Instructor Guide

This is the two-hour version of Module 4. It tells the same story with the same code and slides as the four-hour module, and keeps its explanations. Instead of pair tasks, **you do every step live with the assistant while the class watches and predicts**.

**Built for one projected screen.** The whole class runs in one VS Code window, on one class workspace that a single command builds before class. Every step is numbered in `class/prompts.md`: copy it, paste it, run it. In this guide, **[prompt N]** marks the moment to copy entry N from `prompts.md`, a chat prompt or a terminal command; whatever comes before it in the step is said or asked first. Moving to the next stage of the story is one command, `python class/go.py STAGE`. On screen you switch between the deck and VS Code, plus a browser tab in blocks 1, 3 and 4. In class, read from the Hebrew transcript on your phone; this guide is for preparation.

**The story in three sentences.**
1. A small feature, optional due dates and an "Overdue" view, forces two decisions: which day counts as "today" (the UTC day), and what clearing a date means.
2. A test written from those decisions catches a clearing bug that the old tests missed.
3. After release, an AI "cleanup" quietly breaks "today" on a server set to local time. Every check passes, because the tests replaced the clock; a test that replaces only the clock catches it.

**How every block works.** You run the step live with the assistant, and the class predicts the result first. Then you point out what the result shows, using "What to point out". Every live call has a fallback: a `go` command, a slide, or something you say. If a reply takes more than about 60 seconds, use the fallback and say so.

**One way of working with the assistant.** Every prompt goes to Copilot Chat in Agent mode. The workspace's rules file (`AGENTS.md`, also in `.github/copilot-instructions.md`) tells the assistant to propose any change to code or tests and wait for approval. So each editing step is two prompts: the request, then a short "go ahead". That is slide 9's order too: plan, approve, edit, review, test. Prompts that only read end with "Do not edit files." Three habits keep the chat clean, and `prompts.md` reminds you of each: start a **new chat** where a step says so, so earlier answers don't carry over; click **Keep** after an edit you approved, before you go on; and keep the current step at the top of `prompts.md`, because later steps give answers away.

**What students need:** nothing. Nobody installs or unzips anything in class.

**After class,** share the student zip (`student/` in the package) together with the four files its guide expects during class: `handouts/feature_contract.md`, `handouts/2_task_c_start.zip`, `handouts/task_e_thread_summary.md` and `handouts/task_f_release_0_4_1.zip`. With those, anyone can do the six tasks at home. The homework uses the four-hour version's fuller support evidence; the answers are at the end of this guide.

## What you use

| Item | Used for |
|---|---|
| `module4_slides_short.pptx` | The deck: the same 20 slides, in a normal slide show (no presenter view needed) |
| `setup_class.py` | Builds the class workspace before class, in one command |
| `class/` | Copied into the workspace, where Git and Copilot ignore it: `prompts.md` (every step), `show/` (two files you show) and the two class tools, `go.py` and `mutant.py`. `class/inputs/support_thread.md` is the source of the thread; the workspace's stages carry it, with the request and the backlog, in a visible `inputs/` folder |
| The Hebrew transcript, on your phone | What to say, step by step |
| This guide | Preparation: the plan, the expected results, what to point out and the fallbacks |

---

## At a glance (two hours, no break)

| Time | Block | Slides | Steps in `prompts.md` |
|---|---|---|---|
| 0:00–0:07 | 1 · Opening | 1–3 | 1 |
| 0:07–0:19 | 2 · Requirements | 4–5 | 2–3 |
| 0:19–0:31 | 3 · Design | 6–8 | 4–5 |
| 0:31–0:57 | 4 · Build and test | 9–11 | 6–17 |
| 0:57–1:07 | 5 · Release | 12–13 | 18–20 |
| 1:07–1:19 | 6 · Maintenance triage | 14–15 | 21–22 |
| 1:19–1:31 | 7 · Close the loop | 16 | 23–30 |
| 1:31–1:39 | 8 · Fix and handoffs | 17 | 31–32 |
| 1:39–1:49 | 9 · Wrap-up | 18–20 | — |
| 1:49–2:00 | Reserve for slow replies and questions | | |

There is no break, so keep the pace steady. If you fall behind, shorten the parts marked *(can shorten)*, never the explanations.

---

## Before class (about 10 minutes)

1. **Your environment.** From the two-hour package folder (the one with `setup_class.py`, `class/` and `code/`):
   ```bash
   python -m venv .venv               # macOS: python3 -m venv .venv
   source .venv/bin/activate          # Windows: .venv\Scripts\Activate.ps1 (PowerShell) or .venv\Scripts\Activate.bat (cmd)
   python -m pip install -r code/3_feature_0.4.0/requirements.lock
   python code/tools/preflight.py
   ```
   Every preflight line should say `OK`; the Node line may say `SKIP`.
2. **The class workspace.** With the environment still active:
   ```bash
   python setup_class.py ../module4_class
   ```
   Put it outside the package, and outside your Git repository if the materials live in one. (In the full instructor package, where this folder is `short_2h/`, run `python short_2h/setup_class.py ../module4_class` from the package folder.) It prints the next steps. Running it again rebuilds the workspace from scratch.
3. **VS Code.** File → Open Folder → `module4_class` (trust it if asked). Open `class/show/three_artifacts.md` and `class/prompts.md` from the Explorer; they stay open as tabs. Open Copilot Chat in Agent mode and choose your model. Open the terminal (Ctrl+\`) and run `python -m pytest -q`: `16 passed` confirms it uses the class environment. The workspace sets 16-point fonts for the projector, saves files automatically, and stops Copilot from sending the open file (usually `prompts.md`) with your prompts; if the chat box still shows a current-file chip, click it off.
4. **The browser.** One tab with the `wireframes.html` address the setup printed. In block 1 you open the app in a second tab.
5. **The deck** in a normal slide show, and **the transcript** on your phone.
6. **Recommended: rehearse once,** end to end, following `prompts.md`. Afterwards, `python class/go.py start` resets the workspace, including any tasks you added in the app. To rebuild it from scratch instead, close VS Code first and run the setup command again.

**On screen in class:** the deck and VS Code. Every command runs in VS Code's terminal, and every prompt goes to Copilot Chat in the same window.

**The stages.** Each `go` first discards unfinished changes in the code, so stop the app (Ctrl+C) and click Keep on any pending chat edits before you run it. It never touches `class/` or the VS Code settings.

| `python class/go.py …` | When | What it loads |
|---|---|---|
| `contract` | Step 3, slide 5 | The agreed contract in `docs/`, and the assistant's rules |
| `clearing` | Step 10, slide 10 | The feature, with the clearing bug planted |
| `0.4.0` | Step 18, block 5 | The release that shipped, with its full test suite |
| `0.4.1` | Step 23, block 7 | The release with the AI cleanup |
| `0.4.2` | Step 31, block 8 | The fixed release; also saves its patch as `inputs/fix_0_4_2.diff` |
| `built` | Fallback, step 9 | The prepared feature, as uncommitted changes to review |
| `clock-test` | Fallback, step 26 | The worked clock test, written but not run |
| `start` | After a rehearsal | The baseline, as before class |

---

## Block 1 · Opening (slides 1–3, 7 min)

**Slide 1 (4 min, with step 1).** Start in VS Code on `class/show/three_artifacts.md`: three one-liners from the same project. Ask which one is right; take two answers. The point: none of them is right or wrong until someone decides, and then the decision has to reach all three.

**Step 1 (30 seconds).** Show the product, the Task Tracker from Modules 2 and 3, with no due dates yet. [prompt 1] Run the app, open http://127.0.0.1:8000/ in the browser, and stop it with Ctrl+C.

**Slides 2 and 3 (3 min).** As in the transcript. On slide 3, ask students to watch for one AI suggestion you reject or revise today; you'll ask about it at the end.

---

## Block 2 · Requirements (slides 4–5, 12 min)

**Slide 4 (2 min).** Frame the request, then ask the class: *"How many missing decisions will the assistant find? More or fewer than this room?"*

**Step 2, live (4 min).** [prompt 2] The assistant reads the stakeholder request and the backlog from `inputs/`. Read the reply aloud. Mark one missing decision it found and one backlog item it tagged well.

*Fallback:* go straight to "What to point out" and name the missing decisions yourself. "Before the current time" sounds complete, but it doesn't say whether a task due today counts, or which clock and timezone apply.

**What to point out (3 min).**
- *Story:* As a team member, I want optional due dates and an Overdue only view, so that I can see unfinished work that needs attention.
- *Open decisions:* calendar day or exact time; which timezone defines "today"; whether a task due today is overdue; whether leaving the date out of an update differs from clearing it; how reminders would be delivered.
- *Backlog:*

| # | Item | Tag | Why |
|---:|---|---|---|
| 1, 10 | Put a deadline on a task / Add a date to the API | keep (merge) | Same item |
| 2 | Make the due date required | reject | Breaks every existing task |
| 3 | Show late work in red | split | A text label is required; color only supports it |
| 4 | Add an Overdue only view | keep | Core of the request |
| 5 | Email reminder every morning | defer | Needs discovery: channel, timing, consent, ownership |
| 6 | Let users remove a deadline | keep | Clearing |
| 7 | Keep old tasks working | keep | Additive migration |
| 8 | Show completed tasks as completed | keep | Completed tasks are never overdue |
| 9 | Make deadlines easy and intuitive | split | Untestable as written; split into concrete items, such as a visible Clear date button and text labels |

- *Example Given/When/Then:* Given an unfinished task due 2026-10-04 and a reference day of 2026-10-04, when I read it, then overdue is false.

**Slide 5 (3 min). Step 3.** Until now the workspace had no contract, so the requirements step couldn't see it. [prompt 3] `go contract` creates `docs/feature_contract.md`; open it and walk the decisions: calendar date, the UTC day, today is not overdue, completed is never overdue, omitted versus explicit null. Compare it with the AI's Given/When/Then: which rule does it touch, and what's different? End on the UTC decision: a deliberate simplification that comes back at the end.

---

## Block 3 · Design (slides 6–8, 12 min)

Both design drafts are live. Each prompt sets a size limit, because without one the assistant tends to draw every file and every branch, and nobody can review that in a few minutes. Review each draft with a short, fixed list of questions, not line by line. If the chat shows Mermaid text instead of a drawing, read the text; at this size it's short.

**Slide 6 (2 min).** Ask: *"Will the assistant invent at least one component that doesn't exist?"* Most people say no.

**Step 4, live (4 min).** [prompt 4] Check the diagram with the four questions on the slide only: which components change, what's new, where "today" comes from, and what a cleared date passes through. A question the diagram can't answer is a finding too. Things to look for: an invented scheduler or notification service, a stored `overdue` column, a rule that reads the browser's clock or has no clock at all, an arrow that runs backwards.

*(Can shorten.)* If the diagram comes out big anyway: a test run without the size limit drew 15 file-level boxes. The four questions still found two problems in a minute. The overdue rule took `now`, and no box said where `now` comes from; and the repository did the overdue filtering, which invites a second clock inside SQL. A big diagram is a good way to make the case for the limit.

*Fallback:* go to slide 7 and name the typical mistakes from the list above.

**Slide 7 (2 min).** The reference design: the change fits inside the existing parts. The browser sends a date or null, the API validates it, the repository stores only the date, and "overdue" is calculated on every read from one clock function that gives today's UTC day. A stored flag would go stale when the day changes or a task is completed. Then follow the clearing path along the bottom line: the browser sends null, the API has to keep it rather than drop it, and the repository saves the cleared date. The proof isn't the response to the update; it's a later read that shows the date is gone. That later read is the whole point of the clearing rule.

**Slide 8 and step 5, live (4 min).** A wireframe should help decide how the feature will be used; a table of states doesn't show how someone enters or clears a date. The slide shows the arrangement the running client uses. The explicit Clear date button matters: emptying a native date field works differently in every browser, and many users never discover it.

[prompt 5] The assistant overwrites `wireframes.html`; refresh the browser tab. Check both layouts with the class:
1. A date can be set when adding a task.
2. Clear date is a visible control for a dated task, not hidden in a menu.
3. There is an Overdue only filter.
4. Status is shown in text (Overdue, Done, "Due" plus the date, No due date), not by colour alone.
5. Nothing is out of scope: no reminders, no times of day.

AI drafts usually fail one of these, most often by marking overdue in red only or by tucking clearing away. *(Can shorten:)* then compare: A puts every control on the row (quick to scan, busy on a long list; the running client uses it); B can make Overdue a tab with a count, but hides the date until a task is selected, and adding a task may no longer set a date in one step.

If the assistant prints the HTML in the chat instead of writing the file, tell it: "Write it to wireframes.html." *Fallback:* slide 8 shows layout A; describe B in one sentence and run the checklist on A.

---

## Block 4 · Build and test (slides 9–11, 26 min)

**Slide 9 · the build (11 min), steps 6–9.** The contract is already in the workspace.
- **Step 6:** [prompt 6] `go contract` first, so the build starts from a clean stage and the wireframe page doesn't show up in the review. Then the assistant plans and waits. Read the plan aloud and look for a file that shouldn't change, a new dependency, or anything outside the contract, such as reminders.
- **Step 7:** [prompt 7] narrow it if needed, and approve. While it edits, explain the order: plan, approve, edit, review against the contract, then test. The edits take a few minutes; **if they aren't done about 5 minutes after you approve (around 0:38), switch to the fallback.**
- When it finishes, **don't open the PATCH code in `app/repository.py`.** It's the next demo.
- *(Can shorten.)* **Step 8:** [prompt 8] ask the assistant for a first review before you show the changes. Whether or not you run it, make the point: that's how many teams now use AI on pull requests, as a fast first reader, not the approver.
- Show the changes in VS Code's Source Control view, which includes new files such as `app/overdue.py`. Walk the four questions on the slide: additive migration, frontend inside the existing modules, overdue strictly before the reference day and never for done tasks, one UTC clock.
- **Step 9:** [prompt 9] run the app, add a date, clear it, stop the server. **If clearing doesn't stick, don't fix it:** "that's exactly the next demo."

*Fallback:* say you'll switch to the prepared result. [prompt 9, last line] `python class/go.py built` discards the unfinished live changes and lays in the prepared feature as uncommitted changes, so you review it in Source Control exactly as if it were live.

**Slide 10 · test first, then fix (10 min), steps 10–15.**
- **Step 10:** [prompt 10] `go clearing` loads the prepared version of the feature with one defect planted, the kind a review can miss. Explain: a PATCH that sends an explicit null doesn't clear the saved date, yet the 16 original tests pass, because they were written before due dates existed. Ask: *"Two of the 16 tests send updates. Will either catch this?"* (No: neither sends a due date.)
- **Step 11: you write the test, not the assistant.** If you ask the assistant first, it finds and fixes the bug in under a minute and nobody learns anything about the requirement. [prompt 11] Paste the test into `tests/test_student_feature.py` and walk through it line by line, asking the class what each assertion should be.
- **Step 12:** [prompt 12] expected `1 failed`, with `assert '2026-10-03' is None`: it fails for the reason we expect. Point at the read after the update: a test that checked only the PATCH response (200) would pass and never catch this.
- **Steps 13 and 14:** [prompt 13] the assistant explains the failure and proposes the smallest fix; read the proposal, then [prompt 14] approve. It may run the suite itself afterwards.
- **Step 15:** [prompt 15] `git diff app/repository.py` shows the one changed line. Naming the file keeps your own uncommitted test out of the diff. The full suite: `17 passed`.

*Fallback:* [prompt 14, last line] `git restore --source 0.4.0 app/repository.py` puts in the fixed line. Then review it as usual, [prompt 15]. The change:
```diff
-        update_data = payload.model_dump(exclude_unset=True, exclude_none=True)
+        update_data = payload.model_dump(exclude_unset=True)
```

**Slide 11 · test plan, test data and checking the tests (5 min), steps 16–17.**
1. *The fix (1 min).* `exclude_none` throws away the explicit null, so the old date survives. `exclude_unset` keeps a supplied null and leaves out only fields that were never sent.
2. *Step 16, live test plan and test data (3 min).* [prompt 16] Prune one repeat with the class, and check one expected result against the contract rather than the code. *Fallback:* the table on the slide.
3. *Step 17, one weak test (1 min).* [prompt 17] `class/show/weak_test_example.py` was written by AI, and it passes. But it only asserts a count, so the wrong single task would pass too. A good test names the exact task it expects, from fixed inputs, with the expected result taken from the contract. Then: "How would we know our tests catch a wrong rule? We test the tests in block 7."

---

## Block 5 · Release (slides 12–13, 10 min)

**Step 18:** [prompt 18] `go 0.4.0` loads the release that shipped, with its full test suite. Everything in this block runs on it.

**Slide 12 (3 min).** Two meanings of "AI in the pipeline": an assistant that writes and reviews the workflow (today), and an agent running inside it (Module 6). On the slide is the AI's draft workflow. Ask: *"What does this workflow not check?"* Give it 30 seconds. It runs only Python, while the change touched four JavaScript modules, the page and the stylesheet, and added frontend tests; the corrected workflow adds a `frontend` job. Close with the three kinds of evidence: a workflow file says what's intended, a local run shows what ran here, and a hosted log shows what ran for one commit.

**Slide 13 (7 min).** Health says the process answers; the business probe checks one product rule against the running server. Ask: *"Name a wrong release this probe would pass."* Take two answers. **Step 19:** [prompt 19] the assistant names one, in four lines or fewer.

**What to point out** (and the fallback if the reply is slow). The probe uses a *completed* past-due task, which is never overdue on any day. So it passes a release that gets "today" wrong around midnight, treats today as overdue, breaks clearing, or breaks the frontend. Keep this list: the next block comes back to it.

**Step 20,** the release rehearsal. [prompt 20] Expected: `34 passed`, then `Local rehearsal passed: full suite, health, completed-task probe, cleanup.` *(Can shorten:)* rollback means restoring the previous code and keeping the data; the new column can stay, because older code ignores it.

---

## Block 6 · Maintenance triage (slides 14–15, 12 min)

**Slide 14 (2 min).** The release went out, and a support thread arrives from the Tel Aviv team. Open `inputs/support_thread.md` for 30 seconds: ten short messages, two of them noise.

**Step 21, live (4 min).** The prompt tells the assistant to read only the thread, so it answers from the evidence, not the code. [prompt 21] Check that the answer kept the exact task, due date and time: one that says "several users reported a problem at night" has lost everything that matters.

*Fallback:* the facts below, read from the thread on screen.

**What to point out (2 min).** Ask first: *"Is this one of the wrong releases from the probe list?"*
- *Facts:* at 21:30 UTC, which is 00:30 in Tel Aviv, task-42 (due 3 October, not done) shows Overdue; the saved date is unchanged; a new task, never edited, behaves the same; the API itself returns `overdue: true`; the server is set to local time, and it and the team's laptops show 00:30 on 4 October; the only change was 0.4.1, an AI-assisted tidy-up; from 03:00 local, which is midnight UTC, everything looks as expected.
- *Hypotheses:* "today" comes from the server's local day (most likely); the edit changed something (ruled out by the task that was never edited); the browser decides overdue itself, from its own clock or a cached value (the timing can't rule it out, because the laptops show the same time as the server; the API's own answer does).
- *Noise:* slow search on the Done tab, and the email reminder request.
- *Discriminating check:* call the real function that decides "today" at a fixed moment just after local midnight (00:30 at UTC+03:00) and compare its answer with the UTC day, 3 October. It doesn't need to wait for the next midnight.

**Slide 15 (4 min), step 22.** The same instant falls on two days: at 21:30 UTC on 3 October, a server clock three hours ahead reads 00:30 on 4 October. [prompt 22] The diff shows what 0.4.1 changed. Apart from the version number, it's one line of logic: the conversion to UTC was dropped, with the import it needed, and the docstring still says UTC. Ask: *"Would a human reviewer have caught this pull request?"* Every check passed because the tests' `client` fixture replaces `get_reference_date` with a fixed 4 October, and the probe uses a completed task. Each check was right about what it covered; nobody tested the piece the tests replaced.

If someone says servers run in UTC: most do, and that's what makes this bug dangerous. On a UTC machine, such as a typical CI runner or cloud server, the dropped conversion changes nothing, so "no behavior change intended" looked true. 0.4.0 didn't depend on the host's timezone; 0.4.1 does, and it fails only on a server that isn't on UTC, like this office's.

---

## Block 7 · Close the loop (slide 16, 12 min)

**Step 23 (1 min):** [prompt 23] `go 0.4.1`. Explain the target: replace only the clock with 00:30 on 4 October at UTC+03:00, call the real "today" function, and expect 3 October.

**Steps 24–26, live (4 min).**
- **Step 24:** [prompt 24] the assistant proposes a test and waits. Read it with the class: only `server_now` is replaced, the time has a timezone, the real `get_reference_date()` is called, and the expected day comes from the contract. Ask: *"Will it pass on 0.4.1?"*
- **Step 25:** [prompt 25] approve. The assistant writes the file and stops.
- **Step 26:** [prompt 26] run it. Expected: it fails with `assert datetime.date(2026, 10, 4) == datetime.date(2026, 10, 3)`. **If it passes instead,** the assistant used the `client` fixture or replaced `get_reference_date`. That's the best possible teaching moment: show which fixture replaced what.

*Fallback:* [prompt 26, last line] `python class/go.py clock-test` writes the worked test into the file. Then run the test with the first line of [prompt 26].

**Steps 27–29, the fix (2 min).** [prompt 27] The assistant explains the result and proposes the smallest fix; [prompt 28] approve it. [prompt 29] `git diff app/main.py` shows the two restored lines, and the full suite gives `35 passed`.

*Fallback:* [prompt 28, last line] `git restore --source 0.4.2 app/main.py` puts in the fixed file. Then review it as usual, [prompt 29]; its diff also shows the version number changing. The change:
```diff
-from datetime import date, datetime
+from datetime import date, datetime, timezone
 ...
-    return server_now().date()
+    return server_now().astimezone(timezone.utc).date()
```

**Step 30, the mutation check (3 min).** Now we test the tests. Mutation testing means changing the code on purpose, in a small, wrong way, and checking that some test notices. Our mutant turns "less than" into "less than or equal" in the overdue rule, so a task due today counts as overdue. Ask: *"Which tests fail? Does our new clock test?"* [prompt 30] Run it. Expected: `Detected`, with the today-boundary, filter and read-time tests failing (`3 failed, 32 passed`). The clock test passes, because it checks which day it is, not the overdue rule. (The tool first checks that the suite is green; if the clock fix didn't go in, it says so instead of running the mutant.)

**Why 34 passing tests missed it (2 min), the question on the slide.** Every API test runs through the `client` fixture, which replaces `get_reference_date`. Replacing it made the tests predictable, and also removed it from what they checked. Common mistakes when writing the clock test: using the `client` fixture (the test can never fail), patching `get_reference_date` itself, a naive datetime without `tzinfo`, and calling `datetime.now()` in the test.

---

## Block 8 · Fix and handoffs (slide 17, 8 min)

**Step 31 (1 min):** [prompt 31] `go 0.4.2` and the rehearsal: `37 passed`. The `go` command also saves the real 0.4.1 → 0.4.2 patch as `inputs/fix_0_4_2.diff`.

**Step 32, live (2 min).** [prompt 32] The assistant reads the real patch and the new tests, not a summary, and drafts three texts for three audiences.

**Review (3 min).** Read each sentence and ask whether the patch or the tests support it; delete anything they don't, such as "improved performance". Good answers look like this, and they're the fallback if the reply is slow:
- *Internal changelog (0.4.2):* Fixed the overdue reference day. 0.4.1 used the server's local date instead of the UTC date. Added regression tests that replace only the clock and call the real reference-day function.
- *User release note:* Overdue labels now change at the agreed time again. In 0.4.1, some tasks showed as overdue a few hours early, shortly after local midnight.
- *README note:* Tasks can have an optional due date (`YYYY-MM-DD`). Send `"due_date": null` to clear it; leaving the field out keeps it. A task is overdue when it isn't done and its date is before the current UTC day. For example, on UTC day 2026-10-04 a task due 2026-10-03 is overdue and one due 2026-10-04 is not.

**The next decision (2 min).** Point at the last item on slide 17, the backlog question: should "today" follow the team's timezone? The team in Tel Aviv works in local days, so for three hours every night the correct product disagrees with their wall clock. Whether the contract should change is a product decision, so it goes back to the backlog, not into a hotfix. If the team chooses local time, store a named zone such as `Asia/Jerusalem`, not a fixed offset, because the offset changes with daylight saving time.

---

## Block 9 · Wrap-up (slides 18–20, 10 min)

**Slide 18 (2 min)** traces the clearing rule through every artifact: the contract's example, the null that travels through the design, the code that keeps a supplied null, the test that reads after the update, and the release note that uses the same example.

**Slide 19 (3 min).** Ask: *"Which AI suggestion did you see me reject or revise today, and would you have?"* Then Modules 5, 6 and 8, as in the transcript.

**Slide 20 (5 min).** The exit question as a class discussion: pick one requirement; name a plausible wrong result, a check that would catch it, and one that would miss it. If the room is quiet, offer:
- **Clearing:** a null update returns 200 but the date survives. Caught by a test that clears and reads again; missed by the original 16 tests and by the probe, which never clears anything.
- **Today:** just after local midnight, a task due yesterday in UTC shows as overdue. Caught by a test that replaces only the clock; missed by every test using the `client` fixture, and by the completed-task probe.

Close by saying you'll share the student zip and the task files after class, for anyone who wants to do the six tasks themselves.

---

## Appendix · Differences from the four-hour module

| Four-hour module | Two-hour version |
|---|---|
| Six pair tasks (A–F) and their debriefs | You run each step live; the class predicts first; the debrief points become "What to point out" |
| Students set up, unzip and commit two task folders | Students need nothing; the student zip and the four task files are shared after class |
| A demo folder plus files from several package folders | One class workspace: every step in `class/prompts.md`, every stage one `go` command |
| A support thread, a request log and a release record (about 35 lines) | One short thread (ten messages) and one moment: 00:30 in Tel Aviv is 21:30 UTC |
| An architecture diagram, a sequence diagram and wireframes | The architecture diagram and the wireframes; the clearing path is explained on slide 7 |
| Two weak tests; the mutant in blocks 4 and 7 | One weak test; the mutant once, in block 7 |
| The CI draft and the corrected workflow, opened side by side | The draft on slide 12; the gap in one sentence |
| Two breaks and a 12-minute reserve | No break; an 11-minute reserve |

## Appendix · Homework answers

The homework is at the end of the Student Guide.
1. **The six tasks:** the answers are the "What to point out" lists in this guide, block by block. Task E uses the fuller evidence in `student/inputs/maintenance/`; its facts add exact times to the ones in block 6.
2. **Reminder discovery:** channel and consent, which timezone "morning" means, retries and duplicates, who owns failed deliveries, and cost. Keep reminders separate from due dates.
3. **Business timezone:** change REQ-04 to a named zone (`Asia/Jerusalem`), keep a single clock, and test both sides of local midnight and the 25 October 2026 clock change (UTC+03:00 to UTC+02:00). On Windows, `zoneinfo` needs the `tzdata` package.
4. **Role handoff:** product gives agreed examples, developers give the change and a design note, QA gives independent expected results, operations gives checks and rollback, and support gives observed facts, all using the same requirement IDs.

## Appendix · Troubleshooting

| Problem | Fix |
|---|---|
| A reply takes more than about 60 seconds | Use the step's fallback and say that it's prepared |
| The assistant asks to run a command | Allow it; the result appears in the terminal |
| The assistant edits before you approve | Review the diff as usual; the next `go` discards anything off-script |
| The assistant writes or changes tests to make them pass | Good teaching moment: reject it (Undo) and point to the rule in `AGENTS.md` |
| The assistant prints the wireframe HTML in the chat | Tell it: "Write it to wireframes.html." |
| `go.py` stops with a Git error | Stop the app (Ctrl+C) and run it again |
| Old content reappears in a file after a `go` | A pending chat edit was undone later. Click Keep before each `go`; run the same `go` again to repair |
| Step 12 or 26 says "no tests ran" | The file wasn't written or saved: save it, or use the step's fallback |
| `class/` files don't show in Ctrl+P, and Copilot can't read them | Both on purpose: `class/` holds `prompts.md`. Open its files from the Explorer |
| Re-running the setup fails on Windows | Close VS Code (its terminal holds the folder open) and run it again |
| Port 8000 is busy | Add `--port 8001` and open that port instead |
| VS Code can't find the environment | `setup_class.py` sets it for the workspace; otherwise run `python -c "import sys; print(sys.executable)"` and paste the path into **Python: Select Interpreter → Enter interpreter path…** |
