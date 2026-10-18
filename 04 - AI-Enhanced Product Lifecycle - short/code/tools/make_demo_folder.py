"""Create and advance the instructor's live demo folder, a Git-tracked copy of the baseline outside the package.

    python code/tools/make_demo_folder.py ../demo_build                 # before class: a fresh baseline
    python code/tools/make_demo_folder.py ../demo_build --add-contract  # before the build demo: commit the contract
    python code/tools/make_demo_folder.py ../demo_build --prepared      # block 4 fallback: the prepared feature

Two-hour version only, so every live step happens in the same VS Code window:
    python code/tools/make_demo_folder.py ../demo_build --load 2_task_c_start   # the test-first fix demo
    python code/tools/make_demo_folder.py ../demo_build --load 4_release_0.4.1  # the missing clock test

The fresh folder has no contract yet, so the requirements and design demos see only what the students'
baseline shows. --prepared discards any unfinished live changes and lays the finished feature
(code/3_feature_0.4.0) over the folder without committing it, so it reviews exactly like a live build.
--load discards unfinished live changes, copies a numbered code folder over the demo folder and commits it,
so `git diff` afterwards shows only what happens live. Run the first command again to start over.

Run it with the class environment active, so VS Code is pointed at that environment's Python.
Works on Windows, macOS and Linux; needs Git on the PATH.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import stat
import subprocess
import sys
from pathlib import Path

CODE = Path(__file__).resolve().parents[1]
CONTRACT = CODE.parent / "handouts" / "feature_contract.md"
IGNORE = shutil.ignore_patterns("__pycache__", ".pytest_cache", ".ruff_cache", "*.db", "*.db-*")
GIT_IDENTITY = ["-c", "user.name=Module 4", "-c", "user.email=module4@example.invalid"]


def _make_writable_and_retry(function, path, _error) -> None:
    # Git marks some files read-only; Windows refuses to delete those until they are made writable.
    os.chmod(path, stat.S_IWRITE)
    function(path)


def git(target: Path, *args: str) -> None:
    subprocess.run(["git", *GIT_IDENTITY, *args], cwd=target, check=True)


def create(target: Path) -> None:
    if target.exists():
        if sys.version_info >= (3, 12):
            shutil.rmtree(target, onexc=_make_writable_and_retry)
        else:
            shutil.rmtree(target, onerror=_make_writable_and_retry)
    shutil.copytree(CODE / "1_baseline", target, ignore=IGNORE)
    # The environment lives in the package, outside this folder, so VS Code would not find it on its own.
    (target / ".vscode").mkdir(exist_ok=True)
    (target / ".vscode" / "settings.json").write_text(
        json.dumps({"python.defaultInterpreterPath": sys.executable}, indent=2) + "\n"
    )
    git(target, "init", "-q")
    git(target, "add", "-A")
    git(target, "commit", "-q", "-m", "Baseline 0.3.0")
    print(f"Demo folder ready: {target}")
    print("Open it in VS Code. Before the build demo, run this command again with --add-contract.")


def add_contract(target: Path) -> None:
    tracked = subprocess.run(
        ["git", "ls-files", "--error-unmatch", "docs/feature_contract.md"], cwd=target, capture_output=True
    )
    if tracked.returncode == 0:
        print("The contract is already committed in this demo folder. The build demo can start.")
        return
    (target / "docs").mkdir(exist_ok=True)
    shutil.copy2(CONTRACT, target / "docs" / "feature_contract.md")
    git(target, "add", "docs/feature_contract.md")
    git(target, "commit", "-q", "-m", "Add the agreed feature contract")
    print("Contract committed as docs/feature_contract.md. The build demo can start.")


def prepared(target: Path) -> None:
    # Start from the last commit, so nothing a half-finished live build left behind mixes into the review.
    git(target, "reset", "-q", "--hard")
    git(target, "clean", "-q", "-fd")
    if not (target / "docs" / "feature_contract.md").exists():
        add_contract(target)
    # Only the feature itself: the CI workflow and README would make the diff longer without teaching more.
    shutil.copytree(
        CODE / "3_feature_0.4.0",
        target,
        ignore=shutil.ignore_patterns(
            "__pycache__", ".pytest_cache", ".ruff_cache", "*.db", "*.db-*", ".github", "README.md"
        ),
        dirs_exist_ok=True,
    )
    print("Prepared feature copied in, not committed; any unfinished live changes were discarded.")
    print("Review it in Source Control, or run: git add -A  then  git diff --staged")


LOADABLE = ("2_task_c_start", "4_release_0.4.1")
CLEARING_PLACEHOLDER = """\
# Write one test for REQ-03 (clearing a date) here, using the existing `client` fixture.
# Write it before asking the assistant for a fix, and run it red first.
"""
CLOCK_PLACEHOLDER = """\
# Write the clock test here: replace only app.main.server_now (for example with pytest's monkeypatch)
# and call the real app.main.get_reference_date().
"""


def load(target: Path, snapshot: str) -> None:
    git(target, "reset", "-q", "--hard")
    git(target, "clean", "-q", "-fd")
    if not (target / "docs" / "feature_contract.md").exists():
        add_contract(target)
    # Keep .github/copilot-instructions.md (the assistant's rules); leave out CI workflows and the README.
    shutil.copytree(
        CODE / snapshot,
        target,
        ignore=shutil.ignore_patterns(
            "__pycache__", ".pytest_cache", ".ruff_cache", "*.db", "*.db-*", "workflows", "README.md"
        ),
        dirs_exist_ok=True,
    )
    tests = target / "tests"
    if snapshot == "2_task_c_start":
        (tests / "test_student_feature.py").write_text(CLEARING_PLACEHOLDER)
    else:
        (tests / "test_student_feature.py").unlink(missing_ok=True)
        (tests / "test_clock_provider.py").write_text(CLOCK_PLACEHOLDER)
    git(target, "add", "-A")
    git(target, "commit", "-q", "-m", f"Load {snapshot}")
    print(f"{snapshot} loaded and committed; any unfinished live changes were discarded.")


def main() -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("folder", help="the demo folder, outside the package (for example ../demo_build)")
    step = parser.add_mutually_exclusive_group()
    step.add_argument(
        "--add-contract", action="store_true", help="before the build demo: commit the agreed contract"
    )
    step.add_argument(
        "--prepared", action="store_true", help="block 4 fallback: copy in the prepared feature"
    )
    step.add_argument("--load", choices=LOADABLE, help="two-hour version: load and commit a code folder")
    args = parser.parse_args()

    target = Path(args.folder).resolve()
    if CODE.parent in target.parents or target == CODE.parent:
        raise SystemExit("Put the demo folder outside the package, so the assistant cannot read the answers.")
    if (args.add_contract or args.prepared or args.load) and not (target / ".git").is_dir():
        raise SystemExit(f"{target} is not a demo folder yet. Create it first, without options.")

    if args.add_contract:
        add_contract(target)
    elif args.prepared:
        prepared(target)
    elif args.load:
        load(target, args.load)
    else:
        create(target)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
