# Task 3.3 (R20): Fix Whisper model cache memory leak

## What changed
- Implemented a size-limited Whisper model cache (LRU, max 2 models) to prevent unbounded memory growth when multiple models are used.
- Added explicit cleanup after transcription finishes (even on errors): `del model_obj` + `gc.collect()` in a `finally` block.

## Files touched
- main.py
