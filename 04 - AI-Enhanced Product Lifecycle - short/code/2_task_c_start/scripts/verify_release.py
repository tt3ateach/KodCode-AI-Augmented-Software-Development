"""Local release rehearsal: full test suite, disposable server, health and one business probe.

The script owns its child server and its temporary SQLite database, and cleans both up.
It does not deploy anything and never touches another running server.
"""

from __future__ import annotations

import json
import os
import socket
import subprocess
import sys
import tempfile
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
STARTUP_SECONDS = 12


class ReleaseCheckFailed(RuntimeError):
    """A release gate failed. Raised explicitly so `python -O` cannot skip it."""


def request(base: str, path: str, method: str = "GET", body: dict | None = None):
    data = None if body is None else json.dumps(body).encode()
    req = Request(base + path, data=data, method=method, headers={"Content-Type": "application/json"})
    with urlopen(req, timeout=2) as response:
        return None if response.status == 204 else json.load(response)


def free_port() -> int:
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        return sock.getsockname()[1]


def wait_for_health(base: str, process: subprocess.Popen, log: Path) -> None:
    deadline = time.monotonic() + STARTUP_SECONDS
    while time.monotonic() < deadline:
        if process.poll() is not None:
            raise ReleaseCheckFailed("Server exited before becoming healthy:\n" + log.read_text())
        try:
            if request(base, "/health").get("status") == "ok":
                return
        except OSError:
            time.sleep(0.1)
    raise ReleaseCheckFailed("Health check timed out:\n" + log.read_text())


def semantic_probe(base: str) -> None:
    """REQ-05 business probe: a completed past-due task must never be overdue."""
    past = (datetime.now(timezone.utc).date() - timedelta(days=2)).isoformat()
    item = request(
        base, "/work-items", "POST", {"title": "Release probe", "status": "done", "due_date": past}
    )
    path = "/work-items/" + item["id"]
    try:
        if request(base, path)["overdue"] is not False:
            raise ReleaseCheckFailed("Probe failed: a completed past-due task is marked overdue.")
        overdue_ids = {row["id"] for row in request(base, "/work-items?overdue_only=true")}
        if item["id"] in overdue_ids:
            raise ReleaseCheckFailed("Probe failed: a completed task appears in Overdue only.")
    finally:
        request(base, path, "DELETE")


def main() -> int:
    subprocess.run([sys.executable, "-m", "pytest", "-q"], cwd=ROOT, check=True)
    # On Windows, antivirus or indexing can hold a just-closed file for a moment; a leftover temp file is harmless.
    with tempfile.TemporaryDirectory(prefix="module4-release-", ignore_cleanup_errors=True) as temp:
        port = free_port()
        base = f"http://127.0.0.1:{port}"
        env = dict(os.environ, WORK_ITEMS_DB=str(Path(temp) / "rehearsal.db"))
        log = Path(temp) / "server.log"
        with log.open("w") as out:
            command = [
                sys.executable,
                "-m",
                "uvicorn",
                "app.main:app",
                "--host",
                "127.0.0.1",
                "--port",
                str(port),
            ]
            process = subprocess.Popen(command, cwd=ROOT, env=env, stdout=out, stderr=subprocess.STDOUT)
            try:
                wait_for_health(base, process, log)
                semantic_probe(base)
                print("Local rehearsal passed: full suite, health, completed-task probe, cleanup.")
            finally:
                process.terminate()
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    process.kill()
                    process.wait()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
