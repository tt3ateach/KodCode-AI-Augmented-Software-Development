# Work Items 0.3.0 · baseline

The product before due dates: the Module 2 Work Items API with the modular Module 3 Task Tracker frontend. Run from this folder with your environment active:

```bash
python -m pytest -q
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Expect `16 passed`. Open http://127.0.0.1:8000/ and stop the server (Ctrl+C) before switching folders. Optional frontend checks, if you have Node: `cd app/static` then `node --test tests/*.test.mjs`.
