"""Pre-class check: runs every code path the class depends on, in temporary copies, in about 20 seconds.

Run from anywhere, with the class environment active:
    python code/tools/preflight.py

Every line should say OK. The Node line says SKIP when Node.js is not installed; that is fine, because the
class never runs the frontend tests live. Nothing in the package is modified.
"""

from __future__ import annotations

import os
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

CODE = Path(__file__).resolve().parents[1]
PACKAGE = CODE.parent
ENV = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")

# The worked Task C test, identical to the one in the Instructor Guide.
TASK_C_TEST = """
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
"""

results: list[tuple[bool, str, str]] = []


def check(ok: bool, name: str, detail: str) -> None:
    results.append((ok, name, detail))
    print(f"{'OK  ' if ok else 'FAIL'}  {name:46} {detail}", flush=True)


def copy(folder: Path, tmp: Path) -> Path:
    target = tmp / folder.name
    shutil.copytree(folder, target, ignore=shutil.ignore_patterns("__pycache__", ".pytest_cache", "*.db"))
    return target


def pytest(folder: Path) -> tuple[int, int]:
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "-q", "--color=no", "-p", "no:cacheprovider"],
        cwd=folder,
        env=ENV,
        capture_output=True,
        text=True,
        timeout=180,
    )
    summary = result.stdout.strip().splitlines()[-1] if result.stdout.strip() else result.stderr[-200:]
    passed = int(m.group(1)) if (m := re.search(r"(\d+) passed", summary)) else 0
    failed = int(m.group(1)) if (m := re.search(r"(\d+) failed", summary)) else 0
    return passed, failed


def expect(name: str, folder: Path, passed: int, failed: int = 0) -> None:
    got = pytest(folder)
    check(got == (passed, failed), name, f"{got[0]} passed, {got[1]} failed (expected {passed}, {failed})")


def main() -> int:
    print(f"Python {sys.version.split()[0]} · package {PACKAGE.name}\n")

    # On Windows, antivirus or indexing can hold a just-closed file for a moment; a leftover temp file is harmless.
    with tempfile.TemporaryDirectory(prefix="module4-preflight-", ignore_cleanup_errors=True) as tmp_name:
        tmp = Path(tmp_name)
        expect("1_baseline", copy(CODE / "1_baseline", tmp), 16)
        with zipfile.ZipFile(PACKAGE / "handouts" / "2_task_c_start.zip") as archive:
            archive.extractall(tmp / "task_c")
        start = tmp / "task_c" / "2_task_c_start"
        expect("Task C handout (zip, defect present)", start, 16)
        (start / "tests" / "test_student_feature.py").write_text(TASK_C_TEST)
        expect("Task C: worked test before the fix", start, 16, 1)
        repo = start / "app" / "repository.py"
        repo.write_text(repo.read_text().replace(", exclude_none=True", ""))
        expect("Task C: after the one-line fix", start, 17)
        feature = copy(CODE / "3_feature_0.4.0", tmp)
        expect("3_feature_0.4.0", feature, 34)
        release = copy(CODE / "4_release_0.4.1", tmp)
        expect("4_release_0.4.1 (the defect escapes)", release, 34)
        shutil.copy2(CODE / "5_fixed_0.4.2" / "tests" / "test_clock_provider.py", release / "tests")
        expect("0.4.1 + the new clock tests", release, 35, 2)
        expect("5_fixed_0.4.2", copy(CODE / "5_fixed_0.4.2", tmp), 37)

        with zipfile.ZipFile(PACKAGE / "handouts" / "task_f_release_0_4_1.zip") as archive:
            archive.extractall(tmp / "task_f")
        expect("Task F handout (zip)", tmp / "task_f" / "task_f_release_0_4_1", 34)

        rehearsal = subprocess.run(
            [sys.executable, "scripts/verify_release.py"],
            cwd=feature,
            env=ENV,
            capture_output=True,
            text=True,
            timeout=180,
        )
        check(
            rehearsal.returncode == 0,
            "Release rehearsal (3_feature_0.4.0)",
            rehearsal.stdout.strip().splitlines()[-1],
        )

        # The two-hour class workspace, built in a throwaway folder: every stage and the class mutant.
        # setup_class.py sits in the two-hour package's root, or in short_2h/ in the instructor package.
        candidates = [PACKAGE / "setup_class.py", PACKAGE / "short_2h" / "setup_class.py"]
        setup_script = next((path for path in candidates if path.exists()), None)
        workspace = tmp / "module4_class"
        setup = subprocess.run(
            [sys.executable, str(setup_script or candidates[-1]), str(workspace)],
            env=ENV,
            capture_output=True,
            text=True,
            errors="replace",
            timeout=180,
        )
        if setup_script is None:
            print("SKIP  Two-hour: class workspace                     no setup_class.py in this package")
        elif setup.returncode != 0:
            check(False, "Two-hour: class workspace", "setup_class.py failed; its last lines:")
            for line in (setup.stdout + setup.stderr).strip().splitlines()[-12:]:
                print("      " + line)
        else:
            stages = [
                ("start", 16, 0),
                ("built", 34, 0),
                ("clearing", 16, 0),
                ("0.4.0", 34, 0),
                ("0.4.1", 34, 0),
                ("clock-test", 34, 1),
                ("0.4.2", 37, 0),
            ]
            wrong = []
            for stage, passed, failed in stages:
                moved = subprocess.run(
                    [sys.executable, "class/go.py", stage], cwd=workspace, env=ENV, capture_output=True
                )
                got = pytest(workspace) if moved.returncode == 0 else None
                if got != (passed, failed):
                    wrong.append(f"{stage}: {got}")
            check(not wrong, "Two-hour: class workspace stages", "; ".join(wrong) or "all 7 as expected")
            subprocess.run(
                [sys.executable, "class/go.py", "0.4.1"], cwd=workspace, env=ENV, capture_output=True
            )
            class_mutant = subprocess.run(
                [sys.executable, "class/mutant.py"], cwd=workspace, env=ENV, capture_output=True, text=True
            )
            check(
                class_mutant.returncode == 0 and "Detected" in class_mutant.stdout,
                "Two-hour: class/mutant.py on 0.4.1",
                "detected" if "Detected" in class_mutant.stdout else "SURVIVED or failed",
            )

    mutant = subprocess.run(
        [sys.executable, str(CODE / "tools" / "mutation_demo.py"), "--only", "today_is_overdue"],
        env=ENV,
        capture_output=True,
        text=True,
        timeout=180,
    )
    check(
        mutant.returncode == 0,
        "Mutation demo (< changed to <=)",
        "detected" if mutant.returncode == 0 else "SURVIVED",
    )

    if shutil.which("node"):
        node = subprocess.run(
            ["node", "--test", "tests/service.test.mjs"],
            cwd=CODE / "3_feature_0.4.0" / "app" / "static",
            capture_output=True,
            text=True,
            timeout=60,
        )
        passed = re.search(r"# pass (\d+)", node.stdout)
        check(
            node.returncode == 0,
            "Frontend tests (Node)",
            f"{passed.group(1) if passed else '?'} passed (expected 6)",
        )
    else:
        print("SKIP  Frontend tests (Node)                         Node is not installed; optional")

    failures = [name for ok, name, _ in results if not ok]
    print(
        "\nAll checks passed. You are ready to teach."
        if not failures
        else f"\n{len(failures)} check(s) failed."
    )
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
