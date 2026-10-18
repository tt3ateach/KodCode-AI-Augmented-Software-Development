"""Mutation check for block 7: does the test suite notice a deliberately wrong overdue rule?

    python class/mutant.py

It copies the code to a temporary folder, runs the suite there as it is, then changes `<` to `<=` in the
overdue rule (so a task due today counts as overdue), runs the suite again and lists the tests the change
broke. If the suite already fails before the change, it stops: fix that first. Your workspace is not touched.
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parents[1]
FILE = "app/overdue.py"
OLD = "item.due_date < reference_date"
NEW = "item.due_date <= reference_date"


def run_suite(folder: Path, database: Path) -> tuple[int, list[str], str]:
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider"],
        cwd=folder,
        env=dict(os.environ, WORK_ITEMS_DB=str(database)),
        capture_output=True,
        text=True,
    )
    lines = result.stdout.splitlines()
    failed = [line.split(" - ")[0].removeprefix("FAILED ") for line in lines if line.startswith("FAILED ")]
    summary = next((line for line in reversed(lines) if " passed" in line or " failed" in line), "")
    return result.returncode, failed, summary.strip("= ") or (result.stdout + result.stderr)[-1500:]


def main() -> int:
    # On Windows, antivirus or indexing can hold a just-closed file for a moment; a leftover temp file is harmless.
    with tempfile.TemporaryDirectory(prefix="module4-mutant-", ignore_cleanup_errors=True) as tmp:
        copy = Path(tmp) / "code"
        shutil.copytree(
            WORKSPACE,
            copy,
            ignore=shutil.ignore_patterns(
                ".git", "class", ".vscode", "__pycache__", ".pytest_cache", "*.db", "*.db-*"
            ),
        )
        target = copy / FILE
        text = target.read_text(encoding="utf-8")
        if text.count(OLD) != 1:
            print(f"Can't find the overdue rule ({OLD!r}) in {FILE}. Is a release with due dates loaded?")
            return 1

        code, failed, summary = run_suite(copy, Path(tmp) / "before.db")
        if code != 0:
            print("The suite already fails before any mutation, so the check can't tell you anything:")
            print("  " + "\n  ".join(failed) if failed else summary)
            print("Fix that first (in block 7: did the clock fix go in?), then run this again.")
            return 1

        target.write_text(text.replace(OLD, NEW), encoding="utf-8")
        print(f"Mutant: in {FILE}, `{OLD}` became `{NEW}`. Running the full suite on a copy...\n")
        code, failed, summary = run_suite(copy, Path(tmp) / "mutant.db")

    if not failed:
        if code == 0:
            print("Not detected: every test still passes with the wrong rule.")
            return 0
        print("pytest could not run:\n" + summary)
        return 1
    print("Detected. These tests fail with the wrong rule:")
    for name in failed:
        print("  " + name)
    print("\n" + summary)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
