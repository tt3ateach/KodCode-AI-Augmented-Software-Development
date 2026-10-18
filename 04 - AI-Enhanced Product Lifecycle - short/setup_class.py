"""Build the two-hour class workspace: one folder, opened in one VS Code window, for the whole class.

    python setup_class.py ../module4_class            # from the two-hour package folder
    python short_2h/setup_class.py ../module4_class   # or from the full instructor package folder

Run it with the class environment active, so VS Code is pointed at that
environment's Python. Put the workspace outside the package (and outside your Git repository, if the
materials live in one). Running it again rebuilds the workspace from scratch; close VS Code first, so
no terminal is holding the folder open.

The workspace is a Git repository whose commits are the stages of the story, tagged start, contract,
built, clearing, 0.4.0, 0.4.1, clock-test and 0.4.2. In class, `python class/go.py STAGE` moves between
them. The inputs/ folder (the request, the backlog and, from 0.4.0 on, the support thread) and wireframes.html
are part of every stage, so the assistant can read and write them. The class/ folder holds the steps
(prompts.md), the two files you show and the two class tools; Git ignores it, so changing stage never touches
it, and the assistant doesn't read it.

Works on Windows, macOS and Linux; needs Git on the PATH.
"""

from __future__ import annotations

import json
import os
import shutil
import stat
import subprocess
import sys
import tempfile
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
# The two-hour package keeps code/, handouts/ and student/ next to this script; the instructor package keeps
# this script in short_2h/, one level below them.
PACKAGE = HERE if (HERE / "code").is_dir() else HERE.parent
CODE = PACKAGE / "code"
CONTRACT = PACKAGE / "handouts" / "feature_contract.md"
STUDENT_INPUTS = PACKAGE / "student" / "inputs"
CLASS_SOURCE = HERE / "class"
# Independent of the instructor's own Git settings: no signing prompts, no hooks, no line-ending changes.
GIT_OPTIONS = [
    "-c", "user.name=Module 4", "-c", "user.email=module4@example.invalid",
    "-c", "commit.gpgsign=false", "-c", "tag.gpgsign=false", "-c", "core.autocrlf=false",
]  # fmt: skip
LOCAL_CONFIG = {
    "core.pager": "cat",  # git diff prints straight to the terminal, with no pager to quit
    "core.autocrlf": "false",
    "commit.gpgsign": "false",
    "tag.gpgsign": "false",
    "user.name": "Module 4",
    "user.email": "module4@example.invalid",
}
NOT_COPIED = ("__pycache__", ".pytest_cache", ".ruff_cache", "*.db", "*.db-*", "README.md", "workflows")

# The assistant's rules for the live class. Code changes need a proposal and an approval first, which is
# why every editing prompt in class/prompts.md is followed by a short "go ahead" prompt. Until the feature
# exists, the rules describe only the baseline, so they don't hand the design prompts the answer.
RULES = """\
# Instructions for AI assistants in this folder

This is a classroom copy of the Work Items API (FastAPI and SQLite) with the Task Tracker frontend.

## Source of truth
- The agreed behavior is in `docs/feature_contract.md` (REQ-01 to REQ-08). If the code and the contract
  disagree, the contract wins. Point out the disagreement instead of changing the contract.

## Rules
- Before changing app code or tests, list the files you intend to change and why, and wait for approval.
- Keep changes small and edit only the files the request names.
- Never delete, skip or weaken an existing test to make the suite pass.
{dates_rule}
- After changing app code, run `python -m pytest -q` and quote the actual result.
- Do not add dependencies.
- Ignore the `class/` folder.

## Layout
{layout}
- `app/static/src/` frontend modules: `state.js`, `render.js`, `service.js`, `apiClient.js`, `app.js`
"""
BASELINE_RULES = RULES.format(
    dates_rule="- Tests use fixed dates. Never use `date.today()` or `datetime.now()` in tests.",
    layout="- `app/models.py` validation · `app/repository.py` SQLite storage · `app/main.py` the endpoints",
)
FEATURE_RULES = RULES.format(
    dates_rule="- Tests use a fixed reference day, 2026-10-04 (see `tests/conftest.py`). Never use `date.today()`"
    " or\n  `datetime.now()` in tests.",
    layout="- `app/models.py` validation · `app/repository.py` SQLite storage · `app/overdue.py` the overdue rule\n"
    "- `app/main.py` endpoints and the clock (`server_now`, `get_reference_date`)",
)

CLEARING_PLACEHOLDER = """\
# Write one test for REQ-03 (clearing a date) here, using the existing `client` fixture.
# Write it before asking the assistant for a fix, and run it red first.
"""

CLOCK_PLACEHOLDER = """\
# Write the clock test here: replace only app.main.server_now (for example with pytest's monkeypatch)
# and call the real app.main.get_reference_date().
"""

WIREFRAME_PLACEHOLDER = """\
<!doctype html>
<meta charset="utf-8">
<title>Wireframes</title>
<body style="font: 20px system-ui, sans-serif; color: #667; margin: 3em">
The assistant's wireframes will appear here. After it writes this file, refresh the page.
</body>
"""

# The support thread arrives with the release (block 6), so the design prompts never see it.
THREAD_STAGES = {"0.4.0", "0.4.1", "clock-test", "0.4.2"}

WORKED_CLOCK_TEST = """\
from datetime import date, datetime, timedelta, timezone

import app.main as main


def test_reference_day_is_utc_after_local_midnight(monkeypatch):
    local_after_midnight = datetime(2026, 10, 4, 0, 30, tzinfo=timezone(timedelta(hours=3)))
    monkeypatch.setattr(main, "server_now", lambda: local_after_midnight)
    assert main.get_reference_date() == date(2026, 10, 3)
"""


def _make_writable_and_retry(function, path, _error) -> None:
    # Git marks some files read-only, and Windows refuses to delete those until they are made writable. Antivirus
    # or indexing can also hold a file for a moment, so try again briefly before giving up.
    for _ in range(20):
        try:
            os.chmod(path, stat.S_IWRITE)
            function(path)
            return
        except FileNotFoundError:
            return
        except PermissionError:
            time.sleep(0.25)
    function(path)


def remove_tree(path: Path) -> None:
    if sys.version_info >= (3, 12):
        shutil.rmtree(path, onexc=_make_writable_and_retry)
    else:
        shutil.rmtree(path, onerror=_make_writable_and_retry)


def git(target: Path, *args: str) -> None:
    subprocess.run(["git", *GIT_OPTIONS, *args], cwd=target, check=True)


def lay(target: Path, snapshot: str) -> None:
    shutil.copytree(CODE / snapshot, target, ignore=shutil.ignore_patterns(*NOT_COPIED), dirs_exist_ok=True)


def write(target: Path, relative: str, text: str) -> None:
    path = target / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def add_contract_and_rules(target: Path, rules: str = FEATURE_RULES) -> None:
    # The two-hour class has no Task A; the class agrees the contract on slide 5.
    contract = CONTRACT.read_text(encoding="utf-8").replace(
        "the class agreed after Task A", "the class agreed"
    )
    write(target, "docs/feature_contract.md", contract)
    write(target, "AGENTS.md", rules)
    write(target, ".github/copilot-instructions.md", rules)


# Each stage: (tag, code snapshot, assistant rules or None, extra files written over the snapshot)
STAGES = [
    ("start", "1_baseline", None, {}),
    ("contract", "1_baseline", BASELINE_RULES, {}),
    ("built", "3_feature_0.4.0", FEATURE_RULES, {}),
    ("clearing", "2_task_c_start", FEATURE_RULES, {"tests/test_student_feature.py": CLEARING_PLACEHOLDER}),
    ("0.4.0", "3_feature_0.4.0", FEATURE_RULES, {}),
    ("0.4.1", "4_release_0.4.1", FEATURE_RULES, {"tests/test_clock_provider.py": CLOCK_PLACEHOLDER}),
    ("clock-test", "4_release_0.4.1", FEATURE_RULES, {"tests/test_clock_provider.py": WORKED_CLOCK_TEST}),
    ("0.4.2", "5_fixed_0.4.2", FEATURE_RULES, {}),
]


def build(target: Path) -> None:
    """Commit every stage and tag it, then check out the first one.

    Each stage is assembled in its own fresh folder and committed from there, so nothing in the workspace is
    deleted and recreated while building: on Windows, antivirus can hold a freshly written file for a moment.
    """
    git_dir = str(target / ".git")
    common = {
        "inputs/stakeholder_request.md": (STUDENT_INPUTS / "stakeholder_request.md").read_text(
            encoding="utf-8"
        ),
        "inputs/messy_backlog.md": (STUDENT_INPUTS / "messy_backlog.md").read_text(encoding="utf-8"),
        "wireframes.html": WIREFRAME_PLACEHOLDER,
    }
    thread = (CLASS_SOURCE / "inputs" / "support_thread.md").read_text(encoding="utf-8")
    with tempfile.TemporaryDirectory(prefix="module4-stages-", ignore_cleanup_errors=True) as tmp:
        for tag, snapshot, rules, extra in STAGES:
            folder = Path(tmp) / tag
            lay(folder, snapshot)
            if rules:
                add_contract_and_rules(folder, rules)
            for relative, text in {**common, **extra}.items():
                write(folder, relative, text)
            if tag in THREAD_STAGES:
                write(folder, "inputs/support_thread.md", thread)
            # Neutral messages: the assistant can read the history, so it shouldn't say where the bugs are.
            stage = ["--git-dir", git_dir, "--work-tree", str(folder)]
            git(folder, *stage, "add", "-A")
            git(folder, *stage, "commit", "-q", "--no-verify", "--allow-empty", "-m", f"Stage {tag}")
            git(folder, *stage, "tag", tag)
    git(target, "reset", "-q", "--hard", "start")


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    target = Path(sys.argv[1]).resolve()
    if PACKAGE == target or PACKAGE in target.parents:
        print(f"Put the workspace outside {PACKAGE.name}, for example next to it: ../module4_class.")
        return 2
    if target.exists():
        if not (target / "class" / "go.py").exists():
            print(f"{target} exists and isn't a class workspace. Choose a new folder name.")
            return 2
        remove_tree(target)

    target.mkdir(parents=True)
    git(target, "init", "-q")
    for key, value in LOCAL_CONFIG.items():
        git(target, "config", key, value)
    # Git ignores the class folder and VS Code's settings, so changing stage never touches them.
    exclude = target / ".git" / "info" / "exclude"
    exclude.parent.mkdir(parents=True, exist_ok=True)
    exclude.write_text("class/\n.vscode/\n", encoding="utf-8")

    # class/inputs is only the source of the support thread; the stages carry it in inputs/.
    shutil.copytree(CLASS_SOURCE, target / "class", ignore=shutil.ignore_patterns("__pycache__", "inputs"))
    settings = {
        # The environment lives outside this folder, so VS Code would not find it on its own.
        "python.defaultInterpreterPath": sys.executable,
        "editor.fontSize": 16,
        "terminal.integrated.fontSize": 16,
        "markdown.preview.fontSize": 16,
        "files.exclude": {"**/__pycache__": True, "**/.pytest_cache": True},
        "search.exclude": {"class/**": True},
        # Pasted tests and edits are saved without a Ctrl+S.
        "files.autoSave": "afterDelay",
        # Don't send the open editor (usually class/prompts.md, with every later prompt) as chat context.
        "chat.implicitContext.enabled": {"panel": "never"},
    }
    write(target, ".vscode/settings.json", json.dumps(settings, indent=2) + "\n")

    build(target)
    subprocess.run([sys.executable, str(target / "class" / "go.py"), "start"], cwd=target, check=True)

    print(f"\nClass workspace ready: {target}")
    print("Before class:")
    print("  1. Open that folder in VS Code (File > Open Folder). Open class/prompts.md and")
    print("     class/show/three_artifacts.md. Open Copilot Chat in Agent mode.")
    print(f"  2. In the browser, open {(target / 'wireframes.html').as_uri()}")
    print("  3. In VS Code's terminal, run: python -m pytest -q   (expect 16 passed)")
    print("  4. To rehearse, follow class/prompts.md; afterwards run: python class/go.py start")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
