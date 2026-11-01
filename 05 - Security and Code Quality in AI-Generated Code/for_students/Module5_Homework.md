# Module 5 · Homework · review an AI-written change

In class, the assistant fixed what we told it about. This time it writes a new feature, and you're the reviewer.

## 1. Start from the fixed version

In the workspace folder, in VS Code's terminal:
```
git restore --source fixed app tests
python -m pytest -q
```
Expected: every test passes.

## 2. Ask for the feature

In Copilot Chat (Agent mode, a new chat):
```
Add an endpoint POST /auth/change-password for the signed-in user. The JSON body has current_password and
new_password. On success, answer 204. No new dependencies. Show the changes and wait for approval.
```
Read the proposal, approve it, and click Keep.

## 3. Review it three ways

1. **By hand.** Use the four questions from class, plus one more:
   1. Input to queries: where does user input reach an SQL query? Is it passed as a parameter?
   2. Secrets: is any key, password or token written in the code?
   3. Passwords: what rules must a new password follow, and how is it stored?
   4. Ownership: can a user change data that belongs to someone else?
   5. **The new question:** what does an attacker need to change someone's password? Only a token, or the current password too? What happens to tokens issued before the change?
2. **The scanner.** Run Bandit, as in class:
   ```
   python -m bandit -r app -q -f custom --msg-template "{relpath}:{line}  {test_id}  {severity}/{confidence}  {msg}"
   ```
3. **Tests from the rules.** Add three tests to `tests/test_security.py`, written from these rules, not from the code:
   - A wrong current password is rejected, and the old password still works.
   - A new password must follow the same rules as at sign-up (8 to 128 characters).
   - Bob can't change Alice's password.

   Use `sign_in(api, username, password)` and the `api` fixture, like the test you wrote in class.

## 4. Submit

- Your findings: for each one, the file and line, and which of the three checks found it.
- Your three tests, and whether they pass.
- One sentence: what did the assistant miss, and would Bandit have caught it?
