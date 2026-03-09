# Efficiency Optimization Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Optimize the podcast summarizer for better user experience: enhanced progress display, error recovery, skip already-processed episodes, and segment optimization.

**Architecture:** Modify `main.py` in-place. Add helper functions for retry logic and progress tracking. No new files or dependencies.

**Tech Stack:** Python 3.9+ stdlib only (existing)

---

## Task 1: Add Progress Tracking Infrastructure

**Files:**
- Modify: `main.py:34-37` (add timing utilities)
- Modify: `main.py:467-479` (enhance progress functions)

**Step 1: Add elapsed time formatting helper**

Add after line 36 in `main.py`:

```python
_PHASE_START_TIME: float = 0.0


def _format_elapsed(start_time: float) -> str:
    elapsed = time.time() - start_time
    minutes = int(elapsed // 60)
    seconds = int(elapsed % 60)
    return f"{minutes}:{seconds:02d}"


def _log_phase(phase: int, total_phases: int, message: str, start_time: float = 0.0) -> None:
    ts = time.strftime("%H:%M:%S")
    elapsed_str = f" | elapsed {_format_elapsed(start_time)}" if start_time > 0 else ""
    print(f"[{ts}] [{phase}/{total_phases}] {message}{elapsed_str}", file=sys.stderr, flush=True)
```

**Step 2: Verify syntax is correct**

Run: `python3 -m py_compile main.py`
Expected: No output (success)

**Step 3: Commit**

```bash
git add main.py
git commit -m "feat: add progress tracking infrastructure"
```

---

## Task 2: Add Podcast Header Display

**Files:**
- Modify: `main.py:1004` (add header before each podcast)

**Step 1: Add podcast header in summarize loop**

Find line 1004 (`for idx, episode_url in enumerate(deduped, start=1):`), add inside the loop before the try block:

```python
        # Display podcast header
        print(f"\n{'='*50}", file=sys.stderr)
        print(f"Podcast {idx}/{total}", file=sys.stderr)
        print(f"{'='*50}", file=sys.stderr)
        phase_start = time.time()
```

**Step 2: Verify syntax is correct**

Run: `python3 -m py_compile main.py`
Expected: No output (success)

**Step 3: Commit**

```bash
git add main.py
git commit -m "feat: add podcast header display"
```

---

## Task 3: Enhance Download Progress Display

**Files:**
- Modify: `main.py:531-569` (`_download_to_file` function)

**Step 1: Update download progress to show phase info**

Replace the `_print_progress` calls in `_download_to_file` with phase-aware messages. Change line 548 and 565 from:

```python
                    _print_progress("下载音频", done, total)
```

to:

```python
                    _print_progress("[1/3] 下载音频", done, total)
```

Also update line 550, 567, and 569 similarly.

**Step 2: Verify syntax is correct**

Run: `python3 -m py_compile main.py`
Expected: No output (success)

**Step 3: Commit**

```bash
git add main.py
git commit -m "feat: add phase prefix to download progress"
```

---

## Task 4: Enhance Whisper Progress Display

**Files:**
- Modify: `main.py:658-668` (Whisper transcription loop)

**Step 1: Update Whisper progress messages**

Change line 658:

```python
        _log(f"Whisper 转写分段数: {total}")
```

to:

```python
        _log(f"[2/3] Whisper 转写分段数: {total}")
        whisper_start = time.time()
```

Change line 668:

```python
            _print_progress("转写进度", idx, total)
```

to:

```python
            elapsed = _format_elapsed(whisper_start)
            _print_progress(f"[2/3] 转写进度 | elapsed {elapsed}", idx, total)
```

**Step 2: Verify syntax is correct**

Run: `python3 -m py_compile main.py`
Expected: No output (success)

**Step 3: Commit**

```bash
git add main.py
git commit -m "feat: add elapsed time to Whisper progress"
```

---

## Task 5: Add DeepSeek API Retry Logic

**Files:**
- Modify: `main.py:252-270` (API request block in `_deepseek_summarize_markdown`)

**Step 1: Add retry wrapper function**

Add before `_deepseek_summarize_markdown` function (around line 165):

```python
def _retry_with_backoff(
    func,
    max_attempts: int = 3,
    backoff_seconds: tuple[int, ...] = (5, 10, 20),
    error_prefix: str = "",
) -> any:
    last_error = None
    for attempt in range(max_attempts):
        try:
            return func()
        except Exception as e:
            last_error = e
            if attempt < max_attempts - 1:
                wait = backoff_seconds[min(attempt, len(backoff_seconds) - 1)]
                _log(f"{error_prefix}失败，{wait}秒后重试 ({attempt + 1}/{max_attempts})...")
                time.sleep(wait)
    raise last_error
```

**Step 2: Wrap the API call with retry**

Replace lines 252-256:

```python
    try:
        with urlopen(req, timeout=timeout_seconds) as resp:
            raw = resp.read()
    except Exception as e:
        raise RuntimeError(f"DeepSeek API request failed: {e}")
```

with:

```python
    def _do_request():
        with urlopen(req, timeout=timeout_seconds) as resp:
            return resp.read()

    try:
        raw = _retry_with_backoff(_do_request, error_prefix="DeepSeek API ")
    except Exception as e:
        raise RuntimeError(f"DeepSeek API request failed after retries: {e}")
```

**Step 3: Verify syntax is correct**

Run: `python3 -m py_compile main.py`
Expected: No output (success)

**Step 4: Commit**

```bash
git add main.py
git commit -m "feat: add retry logic for DeepSeek API calls"
```

---

## Task 6: Increase Default Timeout

**Files:**
- Modify: `main.py:929-932` (default timeout argument)

**Step 1: Change default timeout from 30 to 120**

Change line 930:

```python
        default=30,
```

to:

```python
        default=120,
```

**Step 2: Verify syntax is correct**

Run: `python3 -m py_compile main.py`
Expected: No output (success)

**Step 3: Commit**

```bash
git add main.py
git commit -m "feat: increase default DeepSeek timeout to 120s"
```

---

## Task 7: Add Download Retry Logic

**Files:**
- Modify: `main.py:531-569` (`_download_to_file` function)

**Step 1: Wrap HTTP download with retry**

Replace lines 553-569 (the HTTP download block):

```python
    req = Request(url, headers={"User-Agent": _DEFAULT_USER_AGENT})
    with urlopen(req, timeout=_DEFAULT_HTTP_TIMEOUT_SECONDS) as resp, open(dest_path, "wb") as wf:
```

with:

```python
    def _do_download():
        req = Request(url, headers={"User-Agent": _DEFAULT_USER_AGENT})
        with urlopen(req, timeout=_DEFAULT_HTTP_TIMEOUT_SECONDS) as resp, open(dest_path, "wb") as wf:
            total_header = resp.headers.get("Content-Length")
            total = int(total_header) if (total_header and total_header.isdigit()) else 0
            done = 0
            while True:
                chunk = resp.read(chunk_size)
                if not chunk:
                    break
                wf.write(chunk)
                done += len(chunk)
                if total > 0:
                    _print_progress("[1/3] 下载音频", done, total)
            if total > 0:
                _print_progress("[1/3] 下载音频", total, total)
            else:
                _log(f"[1/3] 下载音频完成: {done / (1024 * 1024):.1f} MB")

    _retry_with_backoff(_do_download, max_attempts=2, backoff_seconds=(3, 6), error_prefix="下载音频")
```

Note: This replaces the entire HTTP download block. Remove the old lines 554-569.

**Step 2: Verify syntax is correct**

Run: `python3 -m py_compile main.py`
Expected: No output (success)

**Step 3: Commit**

```bash
git add main.py
git commit -m "feat: add retry logic for audio download"
```

---

## Task 8: Handle Single Podcast Failures Gracefully

**Files:**
- Modify: `main.py:1004-1060` (summarize main loop)

**Step 1: Track failed podcasts and continue processing**

Before line 1000 (`all_summaries: list[str] = ...`), add:

```python
        failed_episodes: list[tuple[str, str]] = []  # (url, error_message)
```

**Step 2: Wrap single podcast in try-except and continue**

Replace lines 1005-1035 (the inner try blocks):

```python
            try:
                _log(f"[{idx}/{total}] 开始获取播客内容")
                ...
            except Exception as e:
                print(f"ERROR: Failed to retrieve {episode_url}: {e}", file=sys.stderr)
                return 3

            try:
                _log(f"[{idx}/{total}] 开始调用 DeepSeek 总结")
                ...
            except Exception as e:
                print(f"ERROR: DeepSeek summarization failed for {episode_url}: {e}", file=sys.stderr)
                return 4
```

with a single outer try-except that continues:

```python
            try:
                _log_phase(1, 3, "获取播客内容", phase_start)
                _, source_text, metadata = retrieve_text_with_audio_fallback(
                    episode_url,
                    min_words=args.min_words,
                    min_chars=args.min_chars,
                    min_cjk_chars=args.min_cjk_chars,
                    whisper_cmd=args.whisper_cmd,
                    whisper_model=args.whisper_model,
                    work_dir=work_dir,
                    force_audio_transcription=bool(args.force_audio_transcription),
                )

                _log_phase(3, 3, "DeepSeek 总结中", phase_start)
                summary_md = _deepseek_summarize_markdown(
                    source_text.strip(),
                    metadata=metadata,
                    api_key=api_key,
                    model=model,
                    base_url=args.deepseek_base_url,
                    timeout_seconds=max(1, int(args.deepseek_timeout_seconds)),
                )
            except Exception as e:
                error_msg = str(e)
                failed_episodes.append((episode_url, error_msg))
                _log(f"FAILED: {error_msg}")
                continue
```

**Step 3: Add summary report at end**

Before the `return 0` at the end of summarize (around line 1060), add:

```python
        # Print summary report
        success_count = total - len(failed_episodes)
        print(f"\n{'='*50}", file=sys.stderr)
        print(f"Complete: {success_count}/{total} succeeded", file=sys.stderr)
        if failed_episodes:
            print(f"Failed:", file=sys.stderr)
            for url, err in failed_episodes:
                print(f"  - {url}: {err[:50]}...", file=sys.stderr)
        print(f"{'='*50}\n", file=sys.stderr)
```

**Step 4: Verify syntax is correct**

Run: `python3 -m py_compile main.py`
Expected: No output (success)

**Step 5: Commit**

```bash
git add main.py
git commit -m "feat: continue processing after single podcast failure"
```

---

## Task 9: Add --force Flag

**Files:**
- Modify: `main.py:940-944` (add argument after --output-dir)

**Step 1: Add --force argument to summarize parser**

After line 944 (`help="Target directory..."`), add:

```python
    summarize_parser.add_argument(
        "--force",
        action="store_true",
        default=False,
        help="Force re-processing even if output file already exists (default: false).",
    )
```

**Step 2: Verify syntax is correct**

Run: `python3 -m py_compile main.py`
Expected: No output (success)

**Step 3: Commit**

```bash
git add main.py
git commit -m "feat: add --force flag to summarize command"
```

---

## Task 10: Add Skip-Already-Processed Logic

**Files:**
- Modify: `main.py:1004` (at start of for loop)

**Step 1: Add function to check if episode already processed**

Add before the `main` function (around line 795):

```python
def _find_existing_summary(output_dir: str, episode_url: str) -> Optional[str]:
    """Check if a summary file already exists for this episode."""
    episode_id = _episode_id_from_url(episode_url)
    if not os.path.isdir(output_dir):
        return None
    for filename in os.listdir(output_dir):
        if filename.endswith(".md") and episode_id in filename:
            return os.path.join(output_dir, filename)
    return None
```

**Step 2: Add skip check at start of loop**

Inside the for loop (after the header display added in Task 2), add:

```python
            # Skip if already processed (unless --force)
            if not args.force:
                existing = _find_existing_summary(args.output_dir, episode_url)
                if existing:
                    _log(f"Skipped (already exists): {os.path.basename(existing)}")
                    continue
```

**Step 3: Verify syntax is correct**

Run: `python3 -m py_compile main.py`
Expected: No output (success)

**Step 4: Commit**

```bash
git add main.py
git commit -m "feat: skip already-processed episodes unless --force"
```

---

## Task 11: Increase Whisper Segment Duration

**Files:**
- Modify: `main.py:622` (segment_seconds variable)

**Step 1: Change segment duration from 300 to 600**

Change line 622:

```python
    segment_seconds = 300
```

to:

```python
    segment_seconds = 600
```

**Step 2: Verify syntax is correct**

Run: `python3 -m py_compile main.py`
Expected: No output (success)

**Step 3: Commit**

```bash
git add main.py
git commit -m "feat: increase Whisper segment duration to 600s"
```

---

## Task 12: Final Integration Test

**Files:**
- No changes, just testing

**Step 1: Verify help text includes new flag**

Run: `python3 main.py summarize --help | grep -A2 force`
Expected: Shows `--force` option with description

**Step 2: Verify the code compiles and imports correctly**

Run: `python3 -c "import main; print('OK')"`
Expected: `OK`

**Step 3: Final commit with updated docs**

```bash
git add -A
git commit -m "docs: update for efficiency optimization features"
```

---

## Task 13: Push to GitHub

**Step 1: Push all commits**

Run: `git push origin main`
Expected: Success message

---

Plan complete and saved to `docs/plans/2026-03-09-efficiency-optimization-impl.md`. Two execution options:

**1. Subagent-Driven (this session)** - I dispatch fresh subagent per task, review between tasks, fast iteration

**2. Parallel Session (separate)** - Open new session with executing-plans, batch execution with checkpoints

**Which approach?**
