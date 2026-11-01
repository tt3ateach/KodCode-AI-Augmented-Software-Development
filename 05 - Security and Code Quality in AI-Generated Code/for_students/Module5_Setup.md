# Module 5 · Setup before class (about 10 minutes)

Do this before class, on the laptop you'll bring. You need Python 3.10 or newer, VS Code with GitHub Copilot, and Git, as in earlier modules.

## 1. Unzip and open

1. Unzip `module5_workspace.zip` to a folder of your choice, for example your course folder. The workspace has a hidden `.git` folder; keep it.
2. In VS Code: File → Open Folder, and choose **the folder that contains `prompts.md`**. On Windows, Extract All may create `module5_workspace\module5_workspace`: open the inner one. If VS Code asks whether you trust the authors, choose Yes.
3. Open the terminal: Terminal → New Terminal.

## 2. Create the environment and install

**Windows (PowerShell):**
```
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.lock
```
If PowerShell refuses to run `Activate.ps1`, run `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` once, then try again.

**macOS or Linux:**
```
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.lock
```

If VS Code asks whether to use the new environment for this workspace, choose Yes.

## 3. Check

```
python scripts/check_setup.py
```

Expected:
```
OK    Python 3.x.x (3.10 or newer)
OK    Packages installed
OK    Git and the workspace's history
OK    Tests: 39 passed in …
OK    Demo data ready in work_items.db: alice / alice-password and bob / bob-password.

Ready for class.
```

If any line says `FAIL`, it says what to do. If that doesn't help, send the output to your instructor before class.

**Please don't read ahead in `prompts.md`.** The class goes through it step by step, and later steps give away the answers to earlier ones.
