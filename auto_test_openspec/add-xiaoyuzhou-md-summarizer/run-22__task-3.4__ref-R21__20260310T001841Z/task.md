# Task 3.4 (R21): Fix incomplete temp audio segment cleanup

## What changed
- Wrapped audio segment processing in `_transcribe_with_python_whisper` with an inner `try/finally`.
- Added guaranteed cleanup call `shutil.rmtree(segment_dir, ignore_errors=True)` so temporary segment files are removed even when transcription fails.

## Files touched
- main.py
