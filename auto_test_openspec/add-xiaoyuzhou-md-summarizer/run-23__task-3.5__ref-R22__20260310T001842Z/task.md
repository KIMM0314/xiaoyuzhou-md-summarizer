# Task 3.5 (R22): Fix HTTP retry logic to skip non-retryable errors

## What changed
- Added `_extract_http_status_code()` helper to parse HTTP status from exceptions.
- Updated `_retry_with_backoff()` to short-circuit and fail fast on HTTP 4xx.
- Kept retries for HTTP 5xx / exceptions without status codes.

## Files touched
- main.py
