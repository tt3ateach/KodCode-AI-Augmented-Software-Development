# Demo 2 · prompts

Use Copilot Chat in **Ask** mode, a new chat for each prompt. Pick the model in the model picker.

## 1 · The clock bug (Module 4), Wi-Fi off

Model: `ministral-3:3b`, then the same prompt to `qwen3.5:9b`.

````
This function must return today's date in UTC (requirement REQ-04). The server runs in Tel Aviv.

```python
from datetime import datetime, timezone

def server_now() -> datetime:
    return datetime.now().astimezone()

def get_reference_date():
    """The calendar day used to decide whether a task is overdue."""
    return server_now().date()
```

Is it correct? Answer in at most three sentences, then give the one-line fix if one is needed.
````

## 2 · Something it has to know, still offline

Model: `qwen3.5:9b`. Paste its function into `israeli_id.py`, then run `python check_id.py`.

```
Write a Python function is_valid_israeli_id(id_str: str) -> bool that checks an Israeli ID number
(up to 9 digits; pad with leading zeros to 9; validate the check digit). Code only, no tests.
```

## 3 · Wi-Fi on, a cloud model

Model: Auto (or any cloud model). Same prompt as 2, paste into `israeli_id.py`, run `python check_id.py` again.
