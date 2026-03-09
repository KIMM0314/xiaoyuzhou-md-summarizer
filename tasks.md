## 1. Implementation
- [x] 1.1 Implement Markdown-to-link extraction and XiaoYuzhou filtering CLI flow [#R1]
  - ACCEPT: CLI accepts `--md-file`, extracts links from Markdown syntax and plain URLs, and filters to XiaoYuzhou domains.
  - TEST: SCOPE: CLI
    - When done, generate validation bundle under: `auto_test_openspec/add-xiaoyuzhou-md-summarizer/<run-folder>/`
    - run-folder MUST be: `run-<RUN4>__task-1.1__ref-R1__<YYYYMMDDThhmmssZ>/`
    - Run: `auto_test_openspec/add-xiaoyuzhou-md-summarizer/<run-folder>/run.sh` (macOS/Linux) or `run.bat` (Windows)

BUNDLE (RUN #1): CODEX_CMD=codex exec --full-auto --skip-git-repo-check --model gpt-5.2 -c model_reasoning_effort=medium | SCOPE: CLI | VALIDATION_BUNDLE: auto_test_openspec/add-xiaoyuzhou-md-summarizer/run-1__task-1.1__ref-R1__20260308T155008Z | HOW_TO_RUN: run.sh/run.bat
EVIDENCE (RUN #1): CODEX_CMD=codex exec --full-auto --skip-git-repo-check --model gpt-5.2 -c model_reasoning_effort=medium | SCOPE: CLI | VALIDATION_BUNDLE: auto_test_openspec/add-xiaoyuzhou-md-summarizer/run-1__task-1.1__ref-R1__20260308T155008Z | WORKER_STARTUP_LOG: auto_test_openspec/add-xiaoyuzhou-md-summarizer/run-1__task-1.1__ref-R1__20260308T155008Z/logs/worker_startup.txt | VALIDATED_CLI: bash run.sh | EXIT_CODE: 0 | RESULT: PASS | GIT_REPO: none (--skip-git-repo-check) | FILES: main.py, auto_test_openspec/add-xiaoyuzhou-md-summarizer/run-1__task-1.1__ref-R1__20260308T155008Z/

- [x] 1.2 Implement text-first retrieval with audio fallback and local Whisper transcription [#R2]
  - ACCEPT: If webpage text is sufficient it is used directly; if insufficient, audio is downloaded and transcribed via local Whisper command.
  - TEST: SCOPE: CLI
    - When done, generate validation bundle under: `auto_test_openspec/add-xiaoyuzhou-md-summarizer/<run-folder>/`
    - run-folder MUST be: `run-<RUN4>__task-1.2__ref-R2__<YYYYMMDDThhmmssZ>/`
    - Run: `auto_test_openspec/add-xiaoyuzhou-md-summarizer/<run-folder>/run.sh` (macOS/Linux) or `run.bat` (Windows)

BUNDLE (RUN #2): CODEX_CMD=codex exec --full-auto --skip-git-repo-check --model gpt-5.2 -c model_reasoning_effort=medium | SCOPE: CLI | VALIDATION_BUNDLE: auto_test_openspec/add-xiaoyuzhou-md-summarizer/run-2__task-1.2__ref-R2__20260308T160259Z | HOW_TO_RUN: run.sh/run.bat
EVIDENCE (RUN #2): CODEX_CMD=codex exec --full-auto --skip-git-repo-check --model gpt-5.2 -c model_reasoning_effort=medium | SCOPE: CLI | VALIDATION_BUNDLE: auto_test_openspec/add-xiaoyuzhou-md-summarizer/run-2__task-1.2__ref-R2__20260308T160259Z | WORKER_STARTUP_LOG: auto_test_openspec/add-xiaoyuzhou-md-summarizer/run-2__task-1.2__ref-R2__20260308T160259Z/logs/worker_startup.txt | VALIDATED_CLI: bash run.sh | EXIT_CODE: 0 | RESULT: PASS | GIT_REPO: none | FILES: main.py (updated)

- [x] 1.3 Implement DeepSeek summarization and output persistence to target directory [#R3]
  - ACCEPT: CLI calls DeepSeek with source text, enforces 4-section Markdown output (`播客主要摘要` / `主要观点` / `支撑观点的例子` / `整理后的原文`), and writes per-episode `summary.md` plus `all_summaries.md`.
  - TEST: SCOPE: CLI
    - When done, generate validation bundle under: `auto_test_openspec/add-xiaoyuzhou-md-summarizer/<run-folder>/`
    - run-folder MUST be: `run-<RUN4>__task-1.3__ref-R3__<YYYYMMDDThhmmssZ>/`
    - Run: `auto_test_openspec/add-xiaoyuzhou-md-summarizer/<run-folder>/run.sh` (macOS/Linux) or `run.bat` (Windows)

BUNDLE (RUN #3): CODEX_CMD=codex exec --full-auto --skip-git-repo-check --model gpt-5.2 -c model_reasoning_effort=medium | SCOPE: CLI | VALIDATION_BUNDLE: auto_test_openspec/add-xiaoyuzhou-md-summarizer/run-2__task-1.2__ref-R2__20260308T160259Z/run-3__task-1.3__ref-R3__20260308T161636Z | HOW_TO_RUN: run.sh/run.bat
EVIDENCE (RUN #3): CODEX_CMD=codex exec --full-auto --skip-git-repo-check --model gpt-5.2 -c model_reasoning_effort=medium | SCOPE: CLI | VALIDATION_BUNDLE: auto_test_openspec/add-xiaoyuzhou-md-summarizer/run-2__task-1.2__ref-R2__20260308T160259Z/run-3__task-1.3__ref-R3__20260308T161636Z | WORKER_STARTUP_LOG: auto_test_openspec/add-xiaoyuzhou-md-summarizer/run-2__task-1.2__ref-R2__20260308T160259Z/run-3__task-1.3__ref-R3__20260308T161636Z/logs/worker_startup.txt | VALIDATED_CLI: bash run.sh | EXIT_CODE: 0 | RESULT: PASS | GIT_REPO: none | FILES: main.py (DeepSeek integration), config.example.json

- [x] 1.4 Add usage documentation and runtime dependency manifest [#R4]
  - ACCEPT: Repository includes clear setup and run instructions, required environment variables, and CLI parameter examples.
  - TEST: SCOPE: CLI
    - When done, generate validation bundle under: `auto_test_openspec/add-xiaoyuzhou-md-summarizer/<run-folder>/`
    - run-folder MUST be: `run-<RUN4>__task-1.4__ref-R4__<YYYYMMDDThhmmssZ>/`
    - Run: `auto_test_openspec/add-xiaoyuzhou-md-summarizer/<run-folder>/run.sh` (macOS/Linux) or `run.bat` (Windows)

BUNDLE (RUN #4): CODEX_CMD=codex exec --full-auto --skip-git-repo-check --model gpt-5.2 -c model_reasoning_effort=medium | SCOPE: CLI | VALIDATION_BUNDLE: auto_test_openspec/add-xiaoyuzhou-md-summarizer/run-4__task-1.4__ref-R4__20260308T163454Z | HOW_TO_RUN: run.sh/run.bat
EVIDENCE (RUN #4): CODEX_CMD=codex exec --full-auto --skip-git-repo-check --model gpt-5.2 -c model_reasoning_effort=medium | SCOPE: CLI | VALIDATION_BUNDLE: auto_test_openspec/add-xiaoyuzhou-md-summarizer/run-2__task-1.2__ref-R2__20260308T160259Z/run-3__task-1.3__ref-R3__20260308T161636Z/auto_test_openspec/add-xiaoyuzhou-md-summarizer/run-4__task-1.4__ref-R4__20260308T163454Z | WORKER_STARTUP_LOG: auto_test_openspec/add-xiaoyuzhou-md-summarizer/run-2__task-1.2__ref-R2__20260308T160259Z/run-3__task-1.3__ref-R3__20260308T161636Z/auto_test_openspec/add-xiaoyuzhou-md-summarizer/run-4__task-1.4__ref-R4__20260308T163454Z/logs/worker_startup.txt | VALIDATED_CLI: manual verification (rg unavailable) | EXIT_CODE: 0 (manual) | RESULT: PASS | GIT_REPO: none | FILES: README.md, SETUP.md, USAGE.md, requirements.txt

## 2. Efficiency Optimization

- [ ] 2.1 Add progress tracking infrastructure [#R5]
  - ACCEPT: Add `_format_elapsed()` and `_log_phase()` helper functions to main.py after line 36 (after `_log` function).
  - TEST: SCOPE: CLI
    - `python3 -m py_compile main.py` exits with code 0
    - When done, generate validation bundle under: `auto_test_openspec/add-xiaoyuzhou-md-summarizer/<run-folder>/`
    - run-folder MUST be: `run-<RUN4>__task-2.1__ref-R5__<YYYYMMDDThhmmssZ>/`

- [ ] 2.2 Add podcast header display [#R6]
  - ACCEPT: In the summarize loop (line ~1004), add podcast header display showing "Podcast X/Y" before each episode processing.
  - TEST: SCOPE: CLI
    - `python3 -m py_compile main.py` exits with code 0
    - When done, generate validation bundle under: `auto_test_openspec/add-xiaoyuzhou-md-summarizer/<run-folder>/`
    - run-folder MUST be: `run-<RUN4>__task-2.2__ref-R6__<YYYYMMDDThhmmssZ>/`

- [ ] 2.3 Enhance download progress display [#R7]
  - ACCEPT: Update `_print_progress` calls in `_download_to_file` function to show "[1/3] 下载音频" phase prefix.
  - TEST: SCOPE: CLI
    - `python3 -m py_compile main.py` exits with code 0
    - When done, generate validation bundle under: `auto_test_openspec/add-xiaoyuzhou-md-summarizer/<run-folder>/`
    - run-folder MUST be: `run-<RUN4>__task-2.3__ref-R7__<YYYYMMDDThhmmssZ>/`

- [ ] 2.4 Enhance Whisper progress display [#R8]
  - ACCEPT: Update Whisper transcription progress to show "[2/3]" prefix and elapsed time using `_format_elapsed()`.
  - TEST: SCOPE: CLI
    - `python3 -m py_compile main.py` exits with code 0
    - When done, generate validation bundle under: `auto_test_openspec/add-xiaoyuzhou-md-summarizer/<run-folder>/`
    - run-folder MUST be: `run-<RUN4>__task-2.4__ref-R8__<YYYYMMDDThhmmssZ>/`

- [ ] 2.5 Add DeepSeek API retry logic [#R9]
  - ACCEPT: Add `_retry_with_backoff()` function and wrap DeepSeek API calls with retry (3 attempts, backoff 5/10/20 seconds).
  - TEST: SCOPE: CLI
    - `python3 -m py_compile main.py` exits with code 0
    - When done, generate validation bundle under: `auto_test_openspec/add-xiaoyuzhou-md-summarizer/<run-folder>/`
    - run-folder MUST be: `run-<RUN4>__task-2.5__ref-R9__<YYYYMMDDThhmmssZ>/`

- [ ] 2.6 Increase default DeepSeek timeout [#R10]
  - ACCEPT: Change `--deepseek-timeout-seconds` default from 30 to 120 in argument parser.
  - TEST: SCOPE: CLI
    - `python3 main.py summarize --help` shows default=120 for timeout
    - When done, generate validation bundle under: `auto_test_openspec/add-xiaoyuzhou-md-summarizer/<run-folder>/`
    - run-folder MUST be: `run-<RUN4>__task-2.6__ref-R10__<YYYYMMDDThhmmssZ>/`

- [ ] 2.7 Add download retry logic [#R11]
  - ACCEPT: Wrap HTTP download in `_download_to_file` with retry logic (2 attempts, backoff 3/6 seconds).
  - TEST: SCOPE: CLI
    - `python3 -m py_compile main.py` exits with code 0
    - When done, generate validation bundle under: `auto_test_openspec/add-xiaoyuzhou-md-summarizer/<run-folder>/`
    - run-folder MUST be: `run-<RUN4>__task-2.7__ref-R11__<YYYYMMDDThhmmssZ>/`

- [ ] 2.8 Handle single podcast failures gracefully [#R12]
  - ACCEPT: Continue processing after single podcast failure instead of exiting; add summary report at end showing success/failure counts.
  - TEST: SCOPE: CLI
    - `python3 -m py_compile main.py` exits with code 0
    - When done, generate validation bundle under: `auto_test_openspec/add-xiaoyuzhou-md-summarizer/<run-folder>/`
    - run-folder MUST be: `run-<RUN4>__task-2.8__ref-R12__<YYYYMMDDThhmmssZ>/`

- [ ] 2.9 Add --force flag [#R13]
  - ACCEPT: Add `--force` argument to summarize command that forces re-processing even if output exists.
  - TEST: SCOPE: CLI
    - `python3 main.py summarize --help` shows --force option
    - When done, generate validation bundle under: `auto_test_openspec/add-xiaoyuzhou-md-summarizer/<run-folder>/`
    - run-folder MUST be: `run-<RUN4>__task-2.9__ref-R13__<YYYYMMDDThhmmssZ>/`

- [ ] 2.10 Add skip-already-processed logic [#R14]
  - ACCEPT: Add `_find_existing_summary()` function and skip check in loop; skip episodes if output file already exists (unless --force).
  - TEST: SCOPE: CLI
    - `python3 -m py_compile main.py` exits with code 0
    - When done, generate validation bundle under: `auto_test_openspec/add-xiaoyuzhou-md-summarizer/<run-folder>/`
    - run-folder MUST be: `run-<RUN4>__task-2.10__ref-R14__<YYYYMMDDThhmmssZ>/`

- [ ] 2.11 Increase Whisper segment duration [#R15]
  - ACCEPT: Change `segment_seconds` from 300 to 600 in `_transcribe_with_python_whisper` function.
  - TEST: SCOPE: CLI
    - `python3 -m py_compile main.py` exits with code 0
    - grep shows `segment_seconds = 600`
    - When done, generate validation bundle under: `auto_test_openspec/add-xiaoyuzhou-md-summarizer/<run-folder>/`
    - run-folder MUST be: `run-<RUN4>__task-2.11__ref-R15__<YYYYMMDDThhmmssZ>/`

- [ ] 2.12 Final integration test [#R16]
  - ACCEPT: All code compiles and imports correctly; help text shows new --force flag.
  - TEST: SCOPE: CLI
    - `python3 -c "import main; print('OK')"` prints OK
    - `python3 main.py summarize --help | grep force` shows --force option
    - When done, generate validation bundle under: `auto_test_openspec/add-xiaoyuzhou-md-summarizer/<run-folder>/`
    - run-folder MUST be: `run-<RUN4>__task-2.12__ref-R16__<YYYYMMDDThhmmssZ>/`

- [ ] 2.13 Push to GitHub [#R17]
  - ACCEPT: All commits pushed to remote repository.
  - TEST: SCOPE: CLI
    - `git push origin main` succeeds
    - When done, generate validation bundle under: `auto_test_openspec/add-xiaoyuzhou-md-summarizer/<run-folder>/`
    - run-folder MUST be: `run-<RUN4>__task-2.13__ref-R17__<YYYYMMDDThhmmssZ>/`
