"""Instructor demo: does the test suite notice a deliberately wrong change?

Each mutant is applied to a disposable copy of a snapshot, the full suite runs, and the script reports
whether the suite failed (the mutant was "detected"). Nothing in the package is modified.

    python code/tools/mutation_demo.py --only today_is_overdue   # Task C debrief: one mutant
    python code/tools/mutation_demo.py                           # three mutants against 0.4.0
    python code/tools/mutation_demo.py --after-maintenance       # adds the clock mutant, against 0.4.2
    python code/tools/mutation_demo.py --only today_is_overdue --folder ../demo_build   # against your live folder
"""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

CODE = Path(__file__).resolve().parents[1]

MUTANTS = [
    (
        "today_is_overdue",
        "app/overdue.py",
        "item.due_date < reference_date",
        "item.due_date <= reference_date",
    ),
    ("completed_is_overdue", "app/overdue.py", "item.status != WorkStatus.done", "True"),
    (
        "null_cannot_clear",
        "app/repository.py",
        "payload.model_dump(exclude_unset=True)",
        "payload.model_dump(exclude_unset=True, exclude_none=True)",
    ),
]
CLOCK_MUTANT = (
    "local_day_provider",
    "app/main.py",
    "return server_now().astimezone(timezone.utc).date()",
    "return server_now().date()",
)


def run_mutant(source: Path, name: str, file: str, old: str, new: str) -> bool:
    # On Windows, antivirus or indexing can hold a just-closed file for a moment; a leftover temp file is harmless.
    with tempfile.TemporaryDirectory(prefix="module4-mutant-", ignore_cleanup_errors=True) as tmp:
        repo = Path(tmp) / "repo"
        shutil.copytree(
            source, repo, ignore=shutil.ignore_patterns("__pycache__", ".pytest_cache", "*.db", ".git")
        )
        target = repo / file
        text = target.read_text()
        if text.count(old) != 1:
            raise SystemExit(f"{name}: expected exactly one {old!r} in {file}")
        target.write_text(text.replace(old, new))
        env = dict(os.environ, WORK_ITEMS_DB=str(Path(tmp) / "default.db"))
        result = subprocess.run(
            [sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider"],
            cwd=repo,
            env=env,
            capture_output=True,
            text=True,
            timeout=120,
        )
        failing = [line.split(" - ")[0] for line in result.stdout.splitlines() if line.startswith("FAILED")]
        # Exit code 1 alone is not enough: "No module named pytest" also exits with 1.
        if result.returncode not in (0, 1) or (result.returncode == 1 and not failing):
            raise SystemExit(f"{name}: pytest could not run\n{result.stdout}{result.stderr}")
        detected = bool(failing)
        print(f"{name:22} {'detected' if detected else 'SURVIVED'}")
        for test in failing:
            print(f"    {test}")
        return detected


def main() -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--after-maintenance", action="store_true", help="use 0.4.2 and add the clock mutant")
    parser.add_argument("--only", help="run a single mutant by name")
    parser.add_argument(
        "--folder", help="run against a copy of this folder instead (for example ../demo_build)"
    )
    args = parser.parse_args()

    snapshot = "5_fixed_0.4.2" if args.after_maintenance else "3_feature_0.4.0"
    source = Path(args.folder).resolve() if args.folder else CODE / snapshot
    if args.folder:
        snapshot = str(source)
    mutants = MUTANTS + ([CLOCK_MUTANT] if args.after_maintenance else [])
    if args.only:
        mutants = [m for m in mutants if m[0] == args.only]
        if not mutants:
            raise SystemExit(f"Unknown mutant: {args.only}")

    print(f"Suite under test: {snapshot if args.folder else 'code/' + snapshot}")
    results = [run_mutant(source, *mutant) for mutant in mutants]
    return 0 if all(results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
