"""Move the class workspace to a stage of the story. Run it from the workspace folder:

    python class/go.py contract      # slide 5: the agreed contract appears in docs/
    python class/go.py clearing      # slide 10: the feature, with the clearing bug planted
    python class/go.py 0.4.0         # block 5: the release that shipped
    python class/go.py 0.4.1         # block 7: the release with the AI cleanup
    python class/go.py 0.4.2         # block 8: the fixed release

Fallbacks, if a live step goes wrong:
    python class/go.py built         # block 4: the prepared feature, as uncommitted changes to review
    python class/go.py clock-test    # block 7: the worked clock test, written but not run

    python class/go.py start         # start over, as before class (also deletes the app's test data)

Every stage first discards unfinished changes in the code. Before you run it, stop the app (Ctrl+C) and
click Keep on any pending edits in the chat, so VS Code doesn't write old content back afterwards.
The class/ folder and VS Code's settings are never touched.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parents[1]

# stage: (checkpoint to reset to, checkpoint to lay over it uncommitted, what to tell the instructor)
STAGES = {
    "start": ("start", None, "Baseline, no contract yet. Ready for blocks 1 and 2."),
    "contract": (
        "contract",
        None,
        "The agreed contract is in docs/feature_contract.md. Open it for slide 5.",
    ),
    "built": (
        "contract",
        "built",
        "The prepared feature is laid in as uncommitted changes. Review it in Source Control, as if it were live.",
    ),
    "clearing": (
        "clearing",
        None,
        "The feature with the clearing bug. Write your test in tests/test_student_feature.py.",
    ),
    "0.4.0": ("0.4.0", None, "Release 0.4.0, as shipped. Ready for block 5."),
    "0.4.1": ("0.4.1", None, "Release 0.4.1, with the AI cleanup. Ready for block 7."),
    "clock-test": (
        "0.4.1",
        "clock-test",
        "The worked clock test is in tests/test_clock_provider.py, not committed. Run it next.",
    ),
    "0.4.2": (
        "0.4.2",
        None,
        "Release 0.4.2, the fix. inputs/fix_0_4_2.diff holds the real patch for block 8.",
    ),
}


def git(*args: str, capture: bool = False) -> str:
    result = subprocess.run(
        ["git", *args], cwd=WORKSPACE, check=True, capture_output=capture, encoding="utf-8", errors="replace"
    )
    return result.stdout if capture else ""


def release_patch() -> str:
    """The real 0.4.1 -> 0.4.2 patch: the code change, and the clock tests as a new file.

    In the workspace, 0.4.1 carries a placeholder test file for the live demo; the shipped 0.4.1 had none.
    """
    code = git("diff", "0.4.1", "0.4.2", "--", "app", capture=True)
    tests = git("show", "0.4.2:tests/test_clock_provider.py", capture=True).splitlines()
    added = "\n".join("+" + line for line in tests)
    return (
        code + "diff --git a/tests/test_clock_provider.py b/tests/test_clock_provider.py\n"
        "new file mode 100644\n--- /dev/null\n+++ b/tests/test_clock_provider.py\n"
        f"@@ -0,0 +1,{len(tests)} @@\n{added}\n"
    )


def main() -> int:
    if len(sys.argv) != 2 or sys.argv[1] not in STAGES:
        print("Usage: python class/go.py STAGE, where STAGE is one of: " + ", ".join(STAGES))
        return 2
    name = sys.argv[1]
    base, overlay, message = STAGES[name]

    if git("status", "--porcelain", capture=True).strip():
        print("Discarding unfinished changes in the code.")
    git("reset", "-q", "--hard", base)
    git("clean", "-q", "-fd")
    if overlay:
        # Lay the overlay's files in without committing them, so they review like live work.
        git("checkout", overlay, "--", ".")
        git("reset", "-q")
    if name == "start":
        for data in WORKSPACE.glob("*.db*"):
            data.unlink()  # tasks added while rehearsing
    if name == "0.4.2":
        # Untracked, in a folder the assistant can read; the next go removes it.
        (WORKSPACE / "inputs" / "fix_0_4_2.diff").write_text(release_patch(), encoding="utf-8")
    print(f"[{name}] {message}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
