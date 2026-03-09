Task 3.2 [#R19]: Add total timeout cap for API calls

Implemented:
- Added `total_timeout` parameter (default 300s) to `_retry_with_backoff()` in `main.py`.
- Tracks total elapsed wall time across all attempts using `time.time()`.
- Raises `TimeoutError` if the total elapsed time exceeds the cap, including checks before each attempt and before sleeping for backoff.
- Updated call sites:
  - DeepSeek API retry uses `total_timeout=300.0`.
  - Audio download retry disables the cap via `total_timeout=None` to avoid limiting long downloads.

Validation:
- `python3 -m py_compile main.py`
- `grep -n "total_timeout" main.py`

