# Module 5 · Security and Code Quality in AI-Generated Code · Instructor Guide

Two hours, no break, code-along. The students do every step on their own laptops while you lead on the projected screen.

**The story in three sentences.**
1. The Task Tracker from Module 4 now has sign-in, written the way AI assistants often write it: it works and every test passes, yet anyone can sign in without a password.
2. The class reviews the code three ways: by hand with four questions, with a scanner, and with an AI review. Each way finds some of the four problems and misses others.
3. A test written from a rule ("Bob can't change Alice's task") catches the problem no scanner sees. The AI fixes everything it's told about, and the class checks what the fix missed.

**Order of the class.** Motivation first: the students break the app themselves in the first 15 minutes. Theory comes after, once they want to know why it happened. Then four short practice blocks, one per kind of check.

**Built for one projected screen.** You need the deck, VS Code and one browser tab. Every command and prompt is a numbered step in the workspace's `prompts.md`. In this guide, **[prompt N]** marks the moment to copy step N; whatever comes before it is said or asked first. In class, read from the Hebrew transcript on your phone; this guide is for preparation.

**Honesty about the code.** The sign-in code was prepared so the four problems are always there. It reproduces mistakes that research keeps finding in AI-generated code, but no assistant wrote this exact file. Say so when you show it (slide 3). Step 4, optional, shows what today's assistant writes.

## What you use

| Item | Used for |
|---|---|
| `module5_slides.pptx` | The deck: 16 slides in a normal slide show, with notes |
| `for_students/module5_workspace.zip` | The class workspace. You use the same one as the students |
| `for_students/Module5_Setup.md` | Send it with the zip, two days before class |
| `for_students/Module5_Homework.md` | Share it after class |
| `transcript/` | The Hebrew transcript: the phone PDF for class, the A4 PDF for printing |
| This guide | Preparation: the plan, the expected results, what to point out, the fallbacks and the homework answers |
| `_build/` | Sources and build scripts. Don't share it |

**Share with students:** the contents of `for_students/`. Nothing else in the package is for them.

---

## At a glance

| Time | Block | Slides | Steps |
|---|---|---|---|
| 0:00–0:05 | Ready | 1 | 1 |
| 0:05–0:20 | **1 · Why this matters** | 2–5 | 2–3 |
| 0:20–0:33 | 2 · Why it happens and how to look | 6–8 | (4, optional) |
| 0:33–0:47 | 3 · Review by hand | 9 | 5 |
| 0:47–0:57 | 4 · The scanner | 10–11 | 6 |
| 0:57–1:07 | 5 · The AI review | 12 | 7 |
| 1:07–1:35 | 6 · Test, fix, check | 13–14 | 8–14 |
| 1:35–1:45 | 7 · Wrap-up | 15–16 | — |
| 1:45–2:00 | Reserve: code-along always runs slow | | |

If you fall behind, shorten the parts marked *(can shorten)*. Never cut block 6: it's where the class sees a fix checked.

**The four problems in the workspace** (`app/auth.py` and `app/main.py`, at the `start` version):

| # | Problem | Where | OWASP Top 10:2025 |
|---|---|---|---|
| 1 | The login query is an f-string built from the username: SQL injection | `auth.py` lines 80–84 | A05 Injection |
| 2 | The token signing key is written in the code | `auth.py` line 24 | A04 Cryptographic Failures (hard-coded key) |
| 3 | No password rules (an empty password works), and passwords are stored as fast, unsalted SHA-256 | `auth.py` lines 30–32 and 41–42 | A07 Authentication Failures; A04 |
| 4 | Any signed-in user can read, change or delete anyone's task by its id. The `user` parameter is there, but never used | `main.py` lines 82–117 | A01 Broken Access Control |

Problem 4 is the important one. The task list is filtered by owner, so the app *looks* right: you only ever see your own tasks. The endpoints that take an id don't check the owner. No pattern in the code is wrong, so no scanner can see it. That's also what happened at Moltbook (slide 5).

---

## Before class

**Two days before:** send the students `for_students/module5_workspace.zip` and `for_students/Module5_Setup.md`. The setup page has them unzip it, open the folder in VS Code, create a `.venv`, install `requirements.lock` and run `python scripts/check_setup.py`. That script checks Python, the packages, Git and the workspace's history, runs the tests and creates the demo users. Ask them to send you the output if any line says `FAIL`.

**Your own setup (about 10 minutes):**
1. Unzip the workspace somewhere outside the package and follow `Module5_Setup.md` yourself. Expected: every line `OK`, then `Ready for class.`
2. In VS Code, zoom in for the projector (Ctrl+= two or three times). Open `prompts.md` and keep it as a tab. Open Copilot Chat in Agent mode and choose your model.
3. In the browser, one tab you'll use for http://127.0.0.1:8000/.
4. **Rehearse once,** end to end, following `prompts.md`. Afterwards, delete the folder and unzip a fresh copy: the rehearsal changes the code, and a fresh copy is the simplest reset.

**On screen in class:** the deck, VS Code and the browser tab.

**How the workspace is built.** It's a Git repository with three tagged versions. `start` is where everyone begins. `fixed` holds the reference fix and the team's security tests; it isn't on the main branch, so it doesn't show up as files in the folder. The class uses it twice, with `git restore --source fixed …`: to catch up after a slow fix, and in step 13 for the team's tests. The workspace's `AGENTS.md` (also in `.github/copilot-instructions.md`) tells the assistant to propose changes and wait for approval, to report reviews without editing, to add no dependencies and to stay off other Git versions.

**Pacing a code-along.** Before each step, say what it does and what to expect. After it, wait until most of the room has the result, not all of it. Anyone behind can copy the catch-up line in `prompts.md` (steps 11 and 13) and rejoin. Students who are ahead can read the next slide's question.

---

## Ready (slide 1, 5 min)

**Slide 1.** While people settle: everyone opens the workspace in VS Code and the terminal. [prompt 1] Expected: five `OK` lines, `Tests: 39 passed`, then `Ready for class.` Anyone with a `FAIL` line pairs with a neighbour for today and fixes the setup after class. That's better than losing the room in the first ten minutes.

---

## Block 1 · Why this matters (slides 2–5, 15 min)

**Slide 2 (6 min). Sign in as anyone.** Say: "In Module 4 we shipped the Task Tracker. Now it has accounts: everyone signs in and sees only their own tasks. The sign-in code is written the way AI assistants often write it. It works, and every test passes." [prompt 2] Everyone starts the app and signs in as `alice` / `alice-password`: two tasks. Sign out.

Then: "Now sign in without knowing anyone's password." [prompt 3] Username `' OR 1=1 --`, password `anything`. Expected: `Welcome, alice.` and Alice's tasks. Then `bob' --`: signed in as Bob. Give the room a minute to enjoy it, then everyone signs out and stops the app with Ctrl+C.

*If the app doesn't start:* the port may be in use (another app, or a second copy). Use `--port 8001` and that address instead.

**Slide 3 (3 min). How it worked.** The left panel is the query in `app/auth.py`: the username goes straight into the SQL text. The right panel is what the database ran: `WHERE username = '' OR 1=1 --' AND password_hash = '…'`. The quote closes the string, `OR 1=1` is true for every row, and `--` turns the password check into a comment. The database returns the first user, Alice. With `bob' --`, it returns Bob.

Say plainly: "This code was prepared for today. It reproduces mistakes that studies keep finding in AI-generated code; no assistant wrote this exact file. The 39 tests check that the features work. None of them asks what an attacker would try."

**Slide 4 (3 min). It isn't just this app.** Three findings, each with its source on the slide:
- Veracode's 2025 GenAI Code Security Report: in 80 coding tasks across more than 100 models, the generated code had a security flaw in 45% of cases. Newer and larger models weren't more secure.
- Perry and others, Stanford, ACM CCS 2023: participants (students and professional developers) with an AI assistant wrote less secure code than those without one. On the SQL task, 36% of the assistant group wrote injectable code, against 7% of the others. They were also *more* confident their code was secure.
- GitGuardian, State of Secrets Sprawl 2025: 6.4% of repositories with Copilot enabled leaked at least one secret, against 4.6% of public repositories overall, a 40% higher rate.

**Slide 5 (3 min). When it ships.** Moltbook is a social network for AI agents. Its founder said publicly that he didn't write a single line of its code. In January 2026, Wiz, a security company, found that its database answered anyone holding the key that ships in the site's own JavaScript. That key is meant to be public; the database was supposed to have access rules saying who may read and change which rows, and it had none. About 1.5 million agent API tokens and 35,000 email addresses were exposed, with full write access. Wiz reported it on 31 January, and it was fixed about three hours later.

Ask: *"Which of today's problems is that?"* The answer comes back in block 3: it's the fourth one, a missing ownership check, not a clever attack.

---

## Block 2 · Why it happens and how to look (slides 6–8, 13 min)

**Slide 6 (4 min). Why assistants write this code.** Four reasons:
1. They learned from public code, and public code is full of insecure examples. Tutorials build SQL with f-strings because it's short.
2. They aim for code that runs and looks right. "Sign-in works" is checked; "sign-in can't be bypassed" isn't, unless someone asks.
3. They don't know your threat model: who might attack, what's sensitive, which user may touch which data. Unless you say it, it isn't in the prompt.
4. People trust the output. The Stanford study's most worrying finding wasn't the bugs, it was the confidence.

**Slide 7 (4 min). Four mistakes to look for,** with their OWASP Top 10:2025 categories. OWASP's Top 10 is the most widely used list of web application risks; its 2025 edition is current.
- Injection (A05): user input becomes part of a query or command. Fix: parameters, never string building.
- Secrets in code (A04, A07): keys and passwords written in the source end up in every copy, every fork and the Git history.
- Weak password handling (A07, A04): no rules for new passwords; fast or unsalted hashes. SHA-256 is fast by design, which is exactly wrong for passwords.
- Broken access control (A01, first on the list): the app checks *who you are* but not *what you may touch*.

Then source and sink, in one sentence: a *source* is where outside input enters (a request body, a URL), a *sink* is where it can do damage (an SQL query, a shell command, a file path). Injection is a path from one to the other with no parameter in between.

**Slide 8 (5 min). Who catches what.** Four kinds of check, and what each can see:
- A **scanner** (static analysis) matches patterns in the code: an f-string that builds SQL, a string assigned to a variable named like a secret, a weak hash function. It runs in seconds, on every commit. It can't know your rules.
- An **AI review** reads the code like a reviewer and explains what it finds. It's good at well-known patterns, but it varies between runs and can't know rules nobody wrote down.
- **Review by hand** with a checklist is slow, but it's the only one that knows the rules: who may see what.
- A **test written from a rule** checks one rule on every run, forever.

Say: "We'll try all four on the same code, and keep score."

**Step 4, optional (3 min, from the reserve).** *(Can shorten.)* "Does today's assistant still do this?" [prompt 4] Read the reply against slide 7. Recent models often use parameters and a salted hash; look for a signing key or secret written in the code ("change-me" is common), no password rules, and nothing about which user may touch which data, because the prompt didn't mention it. Whatever it shows, the point is the same: what it gets right depends on the model and the prompt, so we check.

---

## Block 3 · Review by hand (slide 9, 14 min)

**Slide 9.** The four questions match slide 7's mistakes. [prompt 5] Students open `app/auth.py` and `app/main.py` and write down a file and line for each question. Give them about 7 minutes; walk around.

**Collect the findings (7 min).** Ask for one finding per question, and show it in the code:
1. *Input to queries:* `auth.py` lines 80–84. The f-string puts `username` (and the hash) into the SQL text. Contrast it with `add_user` a few lines up, which uses `?` parameters: the same file does it right once and wrong once.
2. *Secrets:* `auth.py` line 24, `SECRET_KEY = "task-tracker-signing-key-2026"`. Anyone who has the code can sign a token for any user, without a password and without SQL injection.
3. *Passwords:* `Credentials` (lines 30–32) accepts any string, including an empty one. `hash_password` (lines 41–42) is plain SHA-256: no salt, so two users with the same password get the same hash, and fast, so guessing billions of passwords per second on a GPU is routine.
4. *Ownership:* in `main.py`, `get_work_item`, `update_work_item` and `delete_work_item` all take `user`, and none of them uses it. Only the list is filtered by owner. The parameter even makes the code *look* checked.

Most rooms find 1 and 2 quickly, 3 partly, and 4 only after the question is asked. That's the point of the question.

---

## Block 4 · The scanner (slides 10–11, 10 min)

**Slide 10 (6 min).** Stay on slide 9 for now: slide 10 shows the answer. Bandit is a free static analysis tool for Python, already in the workspace. Ask first: *"Which of our four findings will it report?"* [prompt 6] Expected, two lines:
```
app/auth.py:24  B105  LOW/MEDIUM  Possible hardcoded password: 'task-tracker-signing-key-2026'
app/auth.py:81  B608  MEDIUM/LOW  Possible SQL injection vector through string-based query construction.
```
On Windows the path prints as `app\auth.py`. Now show slide 10. Each line shows the rule, then severity/confidence. Point out "Possible" and the low confidence: a scanner matches patterns; it can't tell whether the input is really from a user. Two of four. It missed:
- the password rules (nothing in the code is a known-bad pattern);
- the SHA-256 hash: Bandit flags MD5 and SHA-1, not SHA-256, which is a strong hash, just the wrong kind for passwords;
- ownership: there's no bad line to match, only a missing one.

**Slide 11 (4 min). Other scanners you'll meet.** *(Can shorten to one sentence.)* Different tools look at different things: code patterns (Bandit, Ruff's security rules, Semgrep), data flow from source to sink (CodeQL, in GitHub code scanning), secrets in commits (GitHub secret scanning, gitleaks), and known-vulnerable or non-existent dependencies (pip-audit, Dependabot). The last one matters with AI: assistants sometimes suggest packages that don't exist, and attackers register those names. All of them run in CI, so they check every change, not just the ones someone remembers to review. None of them knows that Bob mustn't change Alice's task.

---

## Block 5 · The AI review (slide 12, 10 min)

**Slide 12.** Ask: *"Will the assistant find the ownership problem?"* [prompt 7] While it answers, compare with the room: every student's reply is different, which is itself a lesson.

**What to point out.** Ask the room: "Who got the SQL injection? The hardcoded key? The password storage? Who got the ownership problem, and in which position?" The first three are almost always there. Ownership varies with the model: missing, lower down, phrased vaguely ("consider authorization"), or clearly named. If most of the room got it, say why: this code leaves a clue, a `user` parameter that's never used. Real missing checks often leave no clue at all, which is why the rule also goes into a test. Rehearse this step with the model the class will use, so you know which case to expect. Assistants are good at patterns they've seen many times. They're less reliable at rules that only exist in your head, and they sometimes add confident findings that don't hold. Ask whether anyone got a finding that's wrong or doesn't matter here.

*If the reply is slow:* go on with the room's answers and slide 12.

---

## Block 6 · Test, fix, check (slides 13–14, 28 min)

**Slide 13 (10 min). Write the rule as a test first.** Say: "Before anyone fixes anything, we write the rule down where it can't be forgotten." [prompt 8] Everyone pastes the test at the end of `tests/test_security.py`. Walk through it: two users; Alice creates a task; Bob tries to change it; the answer must be 403 or 404, and Alice's task must be unchanged. Explain the two codes: 404 is often preferred, because it doesn't even confirm that the task exists.

[prompt 9] Expected: `1 failed`, with `assert 200 in (403, 404)`. It fails for the right reason: Bob's change succeeded.

**The fix (8 min).** Say: "Now the assistant fixes everything we found. Notice the prompt: it names each problem and the fix we want." [prompt 10] Read the proposal with the class: parameters in the query, the key from an environment variable, the password rules, scrypt with a salt, owner checks. Check one thing aloud: what happens to the key when the variable isn't set? Then [prompt 11] approve and click Keep.

*Fallback, and catch-up for anyone behind:* [prompt 11, last line] `git restore --source fixed app` puts in the reference fix.

[prompt 12] Expected: every test passes (`40 passed`, or more if the assistant added tests), and Bandit prints nothing, which means no findings. "Green tests, a clean scan. Done?"

**Slide 14 (10 min). What did the fix miss?** [prompt 13] The team's security tests, one per finding. The first is the student's own test from step 8. Expected with a complete fix: `6 passed`. Typical failures, and what they mean:
- `test_the_signing_key_is_not_fixed_in_the_code`: the fix reads the variable but falls back to a key in the code, for example `os.getenv("TASK_TRACKER_SECRET_KEY", "dev-secret")`. Bandit doesn't flag that. On any server where nobody sets the variable, the key is still in the code. The reference fix makes a random key at startup instead.
- `test_bob_cannot_read_or_delete_alices_task`: the owner check went into the update only. Our own test checked the update, so it passed.
- A password test: different rules from the ones asked for.

Anyone with a failure can use the catch-up line and rejoin.

Then the second miss, which no test here catches. Slide 14's last card asks the question; don't answer it yet. [prompt 14] Start the app and reload the page (sign out if it still shows a user); `' OR 1=1 --` now gets "Invalid username or password." Then sign in as `alice` / `alice-password`: that fails too. Ask: *"Why can't Alice sign in?"* Her password was stored as SHA-256 before the fix, and the fixed code only understands scrypt. On a real system, every existing user would be locked out on release day. Real fixes plan for it: accept the old hash once, then rehash; or ask for a password reset. In class, stop the app, run `python scripts/demo_data.py` (the second part of step 14) to recreate the demo users, start the app again, and sign in. Some assistants handle old hashes on their own; if Alice can sign in straight away, read how the fix did it.

---

## Block 7 · Wrap-up (slides 15–16, 10 min)

**Slide 15 (4 min). The scorecard.** Fill it in with the room's results, then compare with the slide:

| Finding | By hand | Bandit | AI review | A test from the rule |
|---|---|---|---|---|
| SQL injection | usually | yes | almost always | team test |
| Signing key in code | usually | yes | almost always | team test (catches a fallback too) |
| Passwords: rules and storage | partly | no | usually | team tests |
| Other users' tasks | with the question | no | sometimes | your test |

No single check found everything; each was right about what it can see. The one that matters most, ownership, needed a person who knows the rule.

**Slide 16 (6 min). A checklist for AI-generated code,** to keep:
1. Ask for security in the prompt: who may do what, where secrets come from, which inputs to distrust.
2. Review the four questions on every change that touches input, secrets, passwords or data ownership.
3. Run a scanner in CI, and read its findings; don't just count them.
4. Write the important rules as tests before the fix.
5. Check the fix with the same questions. A security fix has side effects, like Alice's password.

Then Module 6, where agents act on their own, plan, test and deploy: every check from today matters more when nobody reads each line. Close with the homework (below): share `Module5_Homework.md`.

---

## Appendix A · Homework and answers

`for_students/Module5_Homework.md` asks students to start from the fixed version (`git restore --source fixed app tests`), ask their assistant for a change-password endpoint with a given prompt, and review it with the four questions plus one, Bandit and three tests from rules. They submit their findings, their tests and one sentence on what the AI missed.

**What to look for in their answers:**
- *Requires the current password?* Assistants often check only that the user is signed in. A stolen token, or a laptop left open, is then enough to take over the account for good.
- *Whose password changes?* If the endpoint takes a username in the body, check that it can't change someone else's: problem 4 again.
- *Rules on the new password:* it should reuse the 8–128 rule. Separate models often forget it.
- *Old tokens:* our tokens are signed and stateless, so tokens issued before the change stay valid until they expire (8 hours). A good answer notices this and suggests shorter token lifetimes or a per-user token version. Full marks for noticing; fixing it isn't required.
- *Bandit:* usually clean. That's the point; good answers say what Bandit couldn't have checked.

**Reference tests** (the endpoint the homework prompt asks for: `POST /auth/change-password` with `current_password` and `new_password`, answering 204):
```python
def test_change_password_needs_the_current_password(api):
    alice = sign_in(api, "alice", "alice-password")
    response = api.post("/auth/change-password", headers=alice,
                        json={"current_password": "wrong-password", "new_password": "new-password-1"})
    assert response.status_code in (400, 401, 403)
    assert api.post("/auth/login", json={"username": "alice", "password": "alice-password"}).status_code == 200


def test_new_password_follows_the_rules(api):
    alice = sign_in(api, "alice", "alice-password")
    response = api.post("/auth/change-password", headers=alice,
                        json={"current_password": "alice-password", "new_password": "short"})
    assert response.status_code in (400, 422)


def test_bob_cannot_change_alices_password(api):
    sign_in(api, "alice", "alice-password")
    bob = sign_in(api, "bob", "bob-password")
    api.post("/auth/change-password", headers=bob,
             json={"username": "alice", "current_password": "bob-password", "new_password": "taken-over-1"})
    assert api.post("/auth/login", json={"username": "alice", "password": "alice-password"}).status_code == 200
```

---

## Appendix B · Troubleshooting

| Symptom | Cause and fix |
|---|---|
| `check_setup.py` says Git isn't installed | Install Git from git-scm.com and reopen VS Code. Until then, the student can do everything except steps 11 (catch-up) and 13 |
| "No Git history here" | The zip was extracted without its hidden `.git` folder, or files were copied out of it. Unzip the whole zip again |
| `python` isn't found, or the wrong Python runs | The `.venv` isn't active. Windows: `.venv\Scripts\Activate.ps1`; macOS: `source .venv/bin/activate`. In VS Code, choose the `.venv` interpreter, then open a new terminal |
| The app says the address is in use | Another copy is running. Stop it with Ctrl+C, or use `--port 8001` |
| Signing in does nothing | The demo users are missing: stop the app, run `python scripts/demo_data.py`, start it again. The script rebuilds the tables, so it also works after a fix changed them |
| The page shows someone signed in, but nothing loads | A session from before the app restarted: reload the page and sign out |
| Bandit prints `app\auth.py` instead of `app/auth.py` | That's Windows; the findings are the same |
| The assistant edits files during a review | Click Undo in the chat, and point out the "Do not edit files" line; the rules file asks for the same |
| The assistant asks to install bcrypt or another package | Say no: the prompt and the rules ask for no new dependencies. `hashlib.scrypt` is in the standard library |
| Tests take much longer after the fix | The assistant chose a much slower password hash. It's correct, just slow in tests; the reference uses scrypt with n=2**14 to keep the suite fast (OWASP's current minimum for scrypt is n=2**17) |
| `ValueError: memory limit exceeded` from `hashlib.scrypt` | The assistant used n=2**17 without raising `maxmem`. Ask it to use n=2**14 as the prompt says, or use the catch-up line |
| PowerShell won't run `Activate.ps1` | `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`, once, then try again |

---

## Sources

- Veracode, *2025 GenAI Code Security Report*, press release of 30 July 2025: https://www.veracode.com/press-release/ai-generated-code-poses-major-security-risks-in-nearly-half-of-all-development-tasks-veracode-research-reveals/
- N. Perry, M. Srivastava, D. Kumar, D. Boneh, *Do Users Write More Insecure Code with AI Assistants?*, ACM CCS 2023: https://arxiv.org/abs/2211.03622
- GitGuardian, *The State of Secrets Sprawl 2025*, as reported by The Hacker News, April 2025: https://thehackernews.com/2025/04/explosive-growth-of-non-human.html
- Wiz, *Hacking Moltbook*, 2 February 2026: https://www.wiz.io/blog/exposed-moltbook-database-reveals-millions-of-api-keys
- OWASP Top 10:2025: https://top10.owasp.org/2025/0x00_2025-Introduction/
- OWASP Password Storage Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html
- Bandit: https://bandit.readthedocs.io/
