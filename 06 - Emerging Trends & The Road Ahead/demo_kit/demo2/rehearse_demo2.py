"""Rehearse Demo 2 on the class laptop, through Ollama directly (not Copilot).

    python rehearse_demo2.py

Checks that the models are installed, that each fits on the GPU, how fast they answer, and whether they
behave as the demo expects:
  1. ministral-3:3b gets the clock bug wrong; qwen3.5:9b gets it right.
  2. qwen3.5:9b writes an Israeli ID validator that fails check_id.py.
Copilot adds its own instructions and doesn't use temperature 0, so also rehearse once in Copilot itself.
Uses only the Python standard library.
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

OLLAMA = os.environ.get("OLLAMA_URL", "http://127.0.0.1:11434")
HERE = Path(__file__).resolve().parent
SMALL, MAIN = "ministral-3:3b", "qwen3.5:9b"
CONTEXT = 16384
CLOCK = (HERE / "prompts.md").read_text(encoding="utf-8").split("````\n")[1].split("````")[0]
ID_PROMPT = (
    "Write a Python function is_valid_israeli_id(id_str: str) -> bool that checks an Israeli ID number\n"
    "(up to 9 digits; pad with leading zeros to 9; validate the check digit). Code only, no tests."
)


def call(path: str, body: dict | None = None) -> dict:
    data = None if body is None else json.dumps(body).encode()
    request = urllib.request.Request(OLLAMA + path, data=data, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(request, timeout=300) as response:
        return json.loads(response.read())


def ask(model: str, prompt: str, limit: int = 900) -> dict:
    body = {"model": model, "prompt": prompt, "stream": False, "think": False,
            "options": {"num_ctx": CONTEXT, "num_predict": limit, "temperature": 0}}
    try:
        return call("/api/generate", body)
    except urllib.error.HTTPError:
        body.pop("think")
        return call("/api/generate", body)


def placement(model: str) -> str:
    for entry in call("/api/ps").get("models", []):
        if entry.get("name") == model:
            share = 100 * entry["size_vram"] / entry["size"]
            return f"{share:.0f}% on the GPU ({entry['size_vram'] / 2**30:.1f} of {entry['size'] / 2**30:.1f} GB)"
    return "not loaded"


def speed(result: dict) -> str:
    return f"{result['eval_count'] / (result['eval_duration'] / 1e9):.0f} tok/s"


def unload(model: str) -> None:
    call("/api/generate", {"model": model, "keep_alive": 0})


def main() -> None:
    try:
        installed = {m["name"] for m in call("/api/tags")["models"]}
    except OSError as error:
        sys.exit(f"Can't reach Ollama at {OLLAMA}: {error}")
    missing = [m for m in (SMALL, MAIN) if m not in installed]
    if missing:
        sys.exit("Pull these first: " + ", ".join(f"ollama pull {m}" for m in missing))

    print(f"1. The clock bug, {SMALL} (expected: says it's correct, or a wrong fix)")
    result = ask(SMALL, CLOCK, 250)
    print(f"   {placement(SMALL)}, {speed(result)}")
    print("   " + result["response"].strip().replace("\n", " ")[:300])
    unload(SMALL)

    print(f"\n   The clock bug, {MAIN} (expected: not correct; use timezone.utc)")
    result = ask(MAIN, CLOCK, 250)
    print(f"   {placement(MAIN)}, {speed(result)}")
    print("   " + result["response"].strip().replace("\n", " ")[:300])

    print(f"\n2. The ID validator, {MAIN} (expected: some checks FAIL)")
    result = ask(MAIN, ID_PROMPT)
    code = "\n\n".join(re.findall(r"```(?:python)?\n(.*?)```", result["response"], re.S)) or result["response"]
    scratch = HERE / "_rehearsal"
    scratch.mkdir(exist_ok=True)
    (scratch / "israeli_id.py").write_text(code, encoding="utf-8")
    (scratch / "check_id.py").write_text((HERE / "check_id.py").read_text(encoding="utf-8"), encoding="utf-8")
    check = subprocess.run([sys.executable, "check_id.py"], cwd=scratch, capture_output=True, text=True)
    print(f"   {speed(result)}; check_id.py says:")
    print("   " + (check.stdout.strip() or check.stderr.strip()).replace("\n", "\n   "))
    unload(MAIN)
    print(f"\nThe model's code is in {scratch / 'israeli_id.py'}. Delete the _rehearsal folder when done.")


if __name__ == "__main__":
    main()
