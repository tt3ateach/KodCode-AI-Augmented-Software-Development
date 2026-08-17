# Module 2 Setup Guide — AI-Assisted Development in Practice

**Version:** v4  
**Validated package date:** 2026-07-12  
**Classroom default:** GitHub Copilot in VS Code or JetBrains IDE

## Required tools

* Python 3.11+; package was smoke-tested on the container's available Python 3.13 runtime, and the code uses only standard Python 3.11+ features.
* Git.
* VS Code or JetBrains IDE.
* GitHub Copilot access.
* Terminal access.
* Browser for the FastAPI docs page.

## Dependency stance

The course is about AI-assisted workflow, not dependency archaeology. For reproducible class labs, the starter and solution repos pin a conservative current stack:

```text
fastapi==0.139.0
uvicorn==0.51.0
pytest==9.1.1
httpx==0.28.1
```

These pins reflect the latest package information checked during v4 generation. The local QA environment already had a compatible stack installed, so the QA report lists the exact runtime versions used there. Revalidate the pinned versions shortly before teaching.

## Starter repo setup

```bash
cd work\_items\_api\_starter
python -m venv .venv
source .venv/bin/activate      # Windows PowerShell: .venv\\Scripts\\Activate.ps1
pip install -r requirements.txt
pytest -q
```

Expected result: tests fail. That is intentional. The starter repo includes behavioral acceptance tests that describe the required API.

## Solution repo setup

```bash
cd work\_items\_api\_solution
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest -q
python -m compileall app
```

Expected result: all tests pass.

## 

