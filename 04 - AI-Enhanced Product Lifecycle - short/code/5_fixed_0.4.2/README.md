# Work Items 0.4.2 · the fixed release (instructor reference)

0.4.2 restores the UTC reference day and adds `tests/test_clock_provider.py`. Those tests replace only the
clock (`server_now`) and call the real `get_reference_date`, so they cover the seam the older fixture
replaced. Run `python -m pytest -q` (37 passed) and `python scripts/verify_release.py`.
