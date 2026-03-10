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

- [x] 2.1 Add progress tracking infrastructure [#R5]
  - ACCEPT: Add `_format_elapsed()` and `_log_phase()` helper functions to main.py after line 36 (after `_log` function).
  - TEST: SCOPE: CLI
    - `python3 -m py_compile main.py` exits with code 0
    - When done, generate validation bundle under: `auto_test_openspec/add-xiaoyuzhou-md-summarizer/<run-folder>/`
    - run-folder MUST be: `run-<RUN4>__task-2.1__ref-R5__<YYYYMMDDThhmmssZ>/`

- [x] 2.2 Add podcast header display [#R6]
  - ACCEPT: In the summarize loop (line ~1004), add podcast header display showing "Podcast X/Y" before each episode processing.
  - TEST: SCOPE: CLI
    - `python3 -m py_compile main.py` exits with code 0
    - When done, generate validation bundle under: `auto_test_openspec/add-xiaoyuzhou-md-summarizer/<run-folder>/`
    - run-folder MUST be: `run-<RUN4>__task-2.2__ref-R6__<YYYYMMDDThhmmssZ>/`

- [x] 2.3 Enhance download progress display [#R7]
  - ACCEPT: Update `_print_progress` calls in `_download_to_file` function to show "[1/3] 下载音频" phase prefix.
  - TEST: SCOPE: CLI
    - `python3 -m py_compile main.py` exits with code 0
    - When done, generate validation bundle under: `auto_test_openspec/add-xiaoyuzhou-md-summarizer/<run-folder>/`
    - run-folder MUST be: `run-<RUN4>__task-2.3__ref-R7__<YYYYMMDDThhmmssZ>/`

- [x] 2.4 Enhance Whisper progress display [#R8]
  - ACCEPT: Update Whisper transcription progress to show "[2/3]" prefix and elapsed time using `_format_elapsed()`.
  - TEST: SCOPE: CLI
    - `python3 -m py_compile main.py` exits with code 0
    - When done, generate validation bundle under: `auto_test_openspec/add-xiaoyuzhou-md-summarizer/<run-folder>/`
    - run-folder MUST be: `run-<RUN4>__task-2.4__ref-R8__<YYYYMMDDThhmmssZ>/`

- [x] 2.5 Add DeepSeek API retry logic [#R9]
  - ACCEPT: Add `_retry_with_backoff()` function and wrap DeepSeek API calls with retry (3 attempts, backoff 5/10/20 seconds).
  - TEST: SCOPE: CLI
    - `python3 -m py_compile main.py` exits with code 0
    - When done, generate validation bundle under: `auto_test_openspec/add-xiaoyuzhou-md-summarizer/<run-folder>/`
    - run-folder MUST be: `run-<RUN4>__task-2.5__ref-R9__<YYYYMMDDThhmmssZ>/`

- [x] 2.6 Increase default DeepSeek timeout [#R10]
  - ACCEPT: Change `--deepseek-timeout-seconds` default from 30 to 120 in argument parser.
  - TEST: SCOPE: CLI
    - `python3 main.py summarize --help` shows default=120 for timeout
    - When done, generate validation bundle under: `auto_test_openspec/add-xiaoyuzhou-md-summarizer/<run-folder>/`
    - run-folder MUST be: `run-<RUN4>__task-2.6__ref-R10__<YYYYMMDDThhmmssZ>/`

- [x] 2.7 Add download retry logic [#R11]
  - ACCEPT: Wrap HTTP download in `_download_to_file` with retry logic (2 attempts, backoff 3/6 seconds).
  - TEST: SCOPE: CLI
    - `python3 -m py_compile main.py` exits with code 0
    - When done, generate validation bundle under: `auto_test_openspec/add-xiaoyuzhou-md-summarizer/<run-folder>/`
    - run-folder MUST be: `run-<RUN4>__task-2.7__ref-R11__<YYYYMMDDThhmmssZ>/`

- [x] 2.8 Handle single podcast failures gracefully [#R12]
  - ACCEPT: Continue processing after single podcast failure instead of exiting; add summary report at end showing success/failure counts.
  - TEST: SCOPE: CLI
    - `python3 -m py_compile main.py` exits with code 0
    - When done, generate validation bundle under: `auto_test_openspec/add-xiaoyuzhou-md-summarizer/<run-folder>/`
    - run-folder MUST be: `run-<RUN4>__task-2.8__ref-R12__<YYYYMMDDThhmmssZ>/`

- [x] 2.9 Add --force flag [#R13]
  - ACCEPT: Add `--force` argument to summarize command that forces re-processing even if output exists.
  - TEST: SCOPE: CLI
    - `python3 main.py summarize --help` shows --force option
    - When done, generate validation bundle under: `auto_test_openspec/add-xiaoyuzhou-md-summarizer/<run-folder>/`
    - run-folder MUST be: `run-<RUN4>__task-2.9__ref-R13__<YYYYMMDDThhmmssZ>/`

- [x] 2.10 Add skip-already-processed logic [#R14]
  - ACCEPT: Add `_find_existing_summary()` function and skip check in loop; skip episodes if output file already exists (unless --force).
  - TEST: SCOPE: CLI
    - `python3 -m py_compile main.py` exits with code 0
    - When done, generate validation bundle under: `auto_test_openspec/add-xiaoyuzhou-md-summarizer/<run-folder>/`
    - run-folder MUST be: `run-<RUN4>__task-2.10__ref-R14__<YYYYMMDDThhmmssZ>/`

- [x] 2.11 Increase Whisper segment duration [#R15]
  - ACCEPT: Change `segment_seconds` from 300 to 600 in `_transcribe_with_python_whisper` function.
  - TEST: SCOPE: CLI
    - `python3 -m py_compile main.py` exits with code 0
    - grep shows `segment_seconds = 600`
    - When done, generate validation bundle under: `auto_test_openspec/add-xiaoyuzhou-md-summarizer/<run-folder>/`
    - run-folder MUST be: `run-<RUN4>__task-2.11__ref-R15__<YYYYMMDDThhmmssZ>/`

- [x] 2.12 Final integration test [#R16]
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

BUNDLE (RUN #5): CODEX_CMD=manual-local-execution | SCOPE: CLI | VALIDATION_BUNDLE: auto_test_openspec/add-xiaoyuzhou-md-summarizer/run-5__task-2.1__ref-R5__20260309T153656Z | HOW_TO_RUN: run.sh/run.bat
EVIDENCE (RUN #5): CODEX_CMD=manual-local-execution | SCOPE: CLI | VALIDATION_BUNDLE: auto_test_openspec/add-xiaoyuzhou-md-summarizer/run-5__task-2.1__ref-R5__20260309T153656Z | WORKER_STARTUP_LOG: auto_test_openspec/add-xiaoyuzhou-md-summarizer/run-5__task-2.1__ref-R5__20260309T153656Z/logs/worker_startup.txt | VALIDATED_CLI: bash run.sh | EXIT_CODE: 0 | RESULT: PASS | FILES: main.py

BUNDLE (RUN #6): CODEX_CMD=manual-local-execution | SCOPE: CLI | VALIDATION_BUNDLE: auto_test_openspec/add-xiaoyuzhou-md-summarizer/run-6__task-2.2__ref-R6__20260309T153656Z | HOW_TO_RUN: run.sh/run.bat
EVIDENCE (RUN #6): CODEX_CMD=manual-local-execution | SCOPE: CLI | VALIDATION_BUNDLE: auto_test_openspec/add-xiaoyuzhou-md-summarizer/run-6__task-2.2__ref-R6__20260309T153656Z | WORKER_STARTUP_LOG: auto_test_openspec/add-xiaoyuzhou-md-summarizer/run-6__task-2.2__ref-R6__20260309T153656Z/logs/worker_startup.txt | VALIDATED_CLI: bash run.sh | EXIT_CODE: 0 | RESULT: PASS | FILES: main.py

BUNDLE (RUN #7): CODEX_CMD=manual-local-execution | SCOPE: CLI | VALIDATION_BUNDLE: auto_test_openspec/add-xiaoyuzhou-md-summarizer/run-7__task-2.3__ref-R7__20260309T153656Z | HOW_TO_RUN: run.sh/run.bat
EVIDENCE (RUN #7): CODEX_CMD=manual-local-execution | SCOPE: CLI | VALIDATION_BUNDLE: auto_test_openspec/add-xiaoyuzhou-md-summarizer/run-7__task-2.3__ref-R7__20260309T153656Z | WORKER_STARTUP_LOG: auto_test_openspec/add-xiaoyuzhou-md-summarizer/run-7__task-2.3__ref-R7__20260309T153656Z/logs/worker_startup.txt | VALIDATED_CLI: bash run.sh | EXIT_CODE: 0 | RESULT: PASS | FILES: main.py

BUNDLE (RUN #8): CODEX_CMD=manual-local-execution | SCOPE: CLI | VALIDATION_BUNDLE: auto_test_openspec/add-xiaoyuzhou-md-summarizer/run-8__task-2.4__ref-R8__20260309T153656Z | HOW_TO_RUN: run.sh/run.bat
EVIDENCE (RUN #8): CODEX_CMD=manual-local-execution | SCOPE: CLI | VALIDATION_BUNDLE: auto_test_openspec/add-xiaoyuzhou-md-summarizer/run-8__task-2.4__ref-R8__20260309T153656Z | WORKER_STARTUP_LOG: auto_test_openspec/add-xiaoyuzhou-md-summarizer/run-8__task-2.4__ref-R8__20260309T153656Z/logs/worker_startup.txt | VALIDATED_CLI: bash run.sh | EXIT_CODE: 0 | RESULT: PASS | FILES: main.py

BUNDLE (RUN #9): CODEX_CMD=manual-local-execution | SCOPE: CLI | VALIDATION_BUNDLE: auto_test_openspec/add-xiaoyuzhou-md-summarizer/run-9__task-2.5__ref-R9__20260309T153656Z | HOW_TO_RUN: run.sh/run.bat
EVIDENCE (RUN #9): CODEX_CMD=manual-local-execution | SCOPE: CLI | VALIDATION_BUNDLE: auto_test_openspec/add-xiaoyuzhou-md-summarizer/run-9__task-2.5__ref-R9__20260309T153656Z | WORKER_STARTUP_LOG: auto_test_openspec/add-xiaoyuzhou-md-summarizer/run-9__task-2.5__ref-R9__20260309T153656Z/logs/worker_startup.txt | VALIDATED_CLI: bash run.sh | EXIT_CODE: 0 | RESULT: PASS | FILES: main.py

BUNDLE (RUN #10): CODEX_CMD=manual-local-execution | SCOPE: CLI | VALIDATION_BUNDLE: auto_test_openspec/add-xiaoyuzhou-md-summarizer/run-10__task-2.6__ref-R10__20260309T153656Z | HOW_TO_RUN: run.sh/run.bat
EVIDENCE (RUN #10): CODEX_CMD=manual-local-execution | SCOPE: CLI | VALIDATION_BUNDLE: auto_test_openspec/add-xiaoyuzhou-md-summarizer/run-10__task-2.6__ref-R10__20260309T153656Z | WORKER_STARTUP_LOG: auto_test_openspec/add-xiaoyuzhou-md-summarizer/run-10__task-2.6__ref-R10__20260309T153656Z/logs/worker_startup.txt | VALIDATED_CLI: bash run.sh | EXIT_CODE: 0 | RESULT: PASS | FILES: main.py

BUNDLE (RUN #11): CODEX_CMD=manual-local-execution | SCOPE: CLI | VALIDATION_BUNDLE: auto_test_openspec/add-xiaoyuzhou-md-summarizer/run-11__task-2.7__ref-R11__20260309T153656Z | HOW_TO_RUN: run.sh/run.bat
EVIDENCE (RUN #11): CODEX_CMD=manual-local-execution | SCOPE: CLI | VALIDATION_BUNDLE: auto_test_openspec/add-xiaoyuzhou-md-summarizer/run-11__task-2.7__ref-R11__20260309T153656Z | WORKER_STARTUP_LOG: auto_test_openspec/add-xiaoyuzhou-md-summarizer/run-11__task-2.7__ref-R11__20260309T153656Z/logs/worker_startup.txt | VALIDATED_CLI: bash run.sh | EXIT_CODE: 0 | RESULT: PASS | FILES: main.py

BUNDLE (RUN #12): CODEX_CMD=manual-local-execution | SCOPE: CLI | VALIDATION_BUNDLE: auto_test_openspec/add-xiaoyuzhou-md-summarizer/run-12__task-2.8__ref-R12__20260309T153656Z | HOW_TO_RUN: run.sh/run.bat
EVIDENCE (RUN #12): CODEX_CMD=manual-local-execution | SCOPE: CLI | VALIDATION_BUNDLE: auto_test_openspec/add-xiaoyuzhou-md-summarizer/run-12__task-2.8__ref-R12__20260309T153656Z | WORKER_STARTUP_LOG: auto_test_openspec/add-xiaoyuzhou-md-summarizer/run-12__task-2.8__ref-R12__20260309T153656Z/logs/worker_startup.txt | VALIDATED_CLI: bash run.sh | EXIT_CODE: 0 | RESULT: PASS | FILES: main.py

BUNDLE (RUN #13): CODEX_CMD=manual-local-execution | SCOPE: CLI | VALIDATION_BUNDLE: auto_test_openspec/add-xiaoyuzhou-md-summarizer/run-13__task-2.9__ref-R13__20260309T153656Z | HOW_TO_RUN: run.sh/run.bat
EVIDENCE (RUN #13): CODEX_CMD=manual-local-execution | SCOPE: CLI | VALIDATION_BUNDLE: auto_test_openspec/add-xiaoyuzhou-md-summarizer/run-13__task-2.9__ref-R13__20260309T153656Z | WORKER_STARTUP_LOG: auto_test_openspec/add-xiaoyuzhou-md-summarizer/run-13__task-2.9__ref-R13__20260309T153656Z/logs/worker_startup.txt | VALIDATED_CLI: bash run.sh | EXIT_CODE: 0 | RESULT: PASS | FILES: main.py

BUNDLE (RUN #14): CODEX_CMD=manual-local-execution | SCOPE: CLI | VALIDATION_BUNDLE: auto_test_openspec/add-xiaoyuzhou-md-summarizer/run-14__task-2.10__ref-R14__20260309T153656Z | HOW_TO_RUN: run.sh/run.bat
EVIDENCE (RUN #14): CODEX_CMD=manual-local-execution | SCOPE: CLI | VALIDATION_BUNDLE: auto_test_openspec/add-xiaoyuzhou-md-summarizer/run-14__task-2.10__ref-R14__20260309T153656Z | WORKER_STARTUP_LOG: auto_test_openspec/add-xiaoyuzhou-md-summarizer/run-14__task-2.10__ref-R14__20260309T153656Z/logs/worker_startup.txt | VALIDATED_CLI: bash run.sh | EXIT_CODE: 0 | RESULT: PASS | FILES: main.py

BUNDLE (RUN #15): CODEX_CMD=manual-local-execution | SCOPE: CLI | VALIDATION_BUNDLE: auto_test_openspec/add-xiaoyuzhou-md-summarizer/run-15__task-2.11__ref-R15__20260309T153656Z | HOW_TO_RUN: run.sh/run.bat
EVIDENCE (RUN #15): CODEX_CMD=manual-local-execution | SCOPE: CLI | VALIDATION_BUNDLE: auto_test_openspec/add-xiaoyuzhou-md-summarizer/run-15__task-2.11__ref-R15__20260309T153656Z | WORKER_STARTUP_LOG: auto_test_openspec/add-xiaoyuzhou-md-summarizer/run-15__task-2.11__ref-R15__20260309T153656Z/logs/worker_startup.txt | VALIDATED_CLI: bash run.sh | EXIT_CODE: 0 | RESULT: PASS | FILES: main.py

BUNDLE (RUN #16): CODEX_CMD=manual-local-execution | SCOPE: CLI | VALIDATION_BUNDLE: auto_test_openspec/add-xiaoyuzhou-md-summarizer/run-16__task-2.12__ref-R16__20260309T153656Z | HOW_TO_RUN: run.sh/run.bat
EVIDENCE (RUN #16): CODEX_CMD=manual-local-execution | SCOPE: CLI | VALIDATION_BUNDLE: auto_test_openspec/add-xiaoyuzhou-md-summarizer/run-16__task-2.12__ref-R16__20260309T153656Z | WORKER_STARTUP_LOG: auto_test_openspec/add-xiaoyuzhou-md-summarizer/run-16__task-2.12__ref-R16__20260309T153656Z/logs/worker_startup.txt | VALIDATED_CLI: bash run.sh | EXIT_CODE: 0 | RESULT: PASS | FILES: main.py

BUNDLE (RUN #17): CODEX_CMD=manual-local-execution | SCOPE: CLI | VALIDATION_BUNDLE: auto_test_openspec/add-xiaoyuzhou-md-summarizer/run-17__task-2.13__ref-R17__20260309T153958Z | HOW_TO_RUN: run.sh/run.bat
EVIDENCE (RUN #17): CODEX_CMD=manual-local-execution | SCOPE: CLI | VALIDATION_BUNDLE: auto_test_openspec/add-xiaoyuzhou-md-summarizer/run-17__task-2.13__ref-R17__20260309T153958Z | WORKER_STARTUP_LOG: auto_test_openspec/add-xiaoyuzhou-md-summarizer/run-17__task-2.13__ref-R17__20260309T153958Z/logs/worker_startup.txt | VALIDATED_CLI: bash run.sh | EXIT_CODE: 128 | RESULT: FAIL | ERROR: fatal: could not read Username for 'https://github.com': Device not configured

BUNDLE (RUN #18): CODEX_CMD=codex exec --full-auto --skip-git-repo-check --model gpt-5.2 -c model_reasoning_effort=medium | SCOPE: CLI | VALIDATION_BUNDLE: auto_test_openspec/add-xiaoyuzhou-md-summarizer/run-18__task-2.13__ref-R17__20260309T213749Z | HOW_TO_RUN: run.sh/run.bat
EVIDENCE (RUN #18): CODEX_CMD=codex exec --full-auto --skip-git-repo-check --model gpt-5.2 -c model_reasoning_effort=medium | SCOPE: CLI | VALIDATION_BUNDLE: auto_test_openspec/add-xiaoyuzhou-md-summarizer/run-18__task-2.13__ref-R17__20260309T213749Z | WORKER_STARTUP_LOG: auto_test_openspec/add-xiaoyuzhou-md-summarizer/run-18__task-2.13__ref-R17__20260309T213749Z/logs/worker_startup.txt | VALIDATED_CLI: bash run.sh | EXIT_CODE: 128 | RESULT: FAIL | ERROR: fatal: could not read Username for 'https://github.com': Device not configured

MAXED (RUN #18, Attempt #2/2): Git push failed AGAIN due to missing GitHub credentials (same error as RUN #17, Attempt #1).
  Error: fatal: could not read Username for 'https://github.com': Device not configured
  Root cause: GitHub credentials not configured (SSH key or HTTPS personal access token).
NEEDS: User must configure GitHub credentials to enable push to remote repository.
  Option 1 (SSH - Recommended):
    - Generate SSH key: ssh-keygen -t ed25519 -C "your_email@example.com"
    - Add public key to GitHub account: Settings → SSH and GPG keys → New SSH key
    - Update remote URL: git remote set-url origin git@github.com:USERNAME/REPO.git
  Option 2 (HTTPS with Personal Access Token):
    - Generate token: GitHub Settings → Developer settings → Personal access tokens → Generate new token
    - Configure credential helper: git config --global credential.helper store
    - On next push, use token as password
  After configuration: Re-run task 2.13 with RUN #19, Attempt #3 (or user may push manually)

## 3. Code Quality Fixes
Note: Based on comprehensive code review identifying critical resource leaks and stability issues.

- [x] 3.1 Fix file handle leak in _read_text_file [#R18]
  - ACCEPT: Replace manual open/read pattern with context manager (with statement) in _read_text_file function at line 161.
  - TEST: SCOPE: CLI
    - `python3 -m py_compile main.py` exits with code 0
    - Grep confirms 'with open(' pattern is used
    - When done, generate validation bundle under: `auto_test_openspec/add-xiaoyuzhou-md-summarizer/<run-folder>/`
    - run-folder MUST be: `run-<RUN#>__task-3.1__ref-R18__<YYYYMMDDThhmmssZ>/`

BUNDLE (RUN #19): CODEX_CMD=codex exec --full-auto --skip-git-repo-check --model gpt-5.2 -c model_reasoning_effort=medium | SCOPE: CLI | VALIDATION_BUNDLE: auto_test_openspec/add-xiaoyuzhou-md-summarizer/run-19__task-3.1__ref-R18__20260309T234431Z/ | HOW_TO_RUN: run.sh/run.bat
EVIDENCE (RUN #19): CODEX_CMD=codex exec --full-auto --skip-git-repo-check --model gpt-5.2 -c model_reasoning_effort=medium | SCOPE: CLI | VALIDATION_BUNDLE: auto_test_openspec/add-xiaoyuzhou-md-summarizer/run-19__task-3.1__ref-R18__20260309T234431Z/ | WORKER_STARTUP_LOG: auto_test_openspec/add-xiaoyuzhou-md-summarizer/run-19__task-3.1__ref-R18__20260309T234431Z/logs/worker_startup.txt | VALIDATED_CLI: bash run.sh | EXIT_CODE: 0 | RESULT: PASS | GIT_COMMIT: 5fa8f1b | COMMIT_MSG: "Fix file handle leak in _read_text_file (task 3.1, R18)" | DIFFSTAT: "7 files changed, 180 insertions(+), 1 deletion(-)" | FILES: main.py (line 161: with open context manager), tasks.md, feature_list.json, validation bundle

- [x] 3.2 Add total timeout cap for API calls [#R19]
  - ACCEPT: Add a total timeout parameter to _retry_with_backoff that caps total time across all retries (e.g. 300 seconds max).
  - TEST: SCOPE: CLI
    - `python3 -m py_compile main.py` exits with code 0
    - Grep confirms timeout cap is implemented
    - When done, generate validation bundle under: `auto_test_openspec/add-xiaoyuzhou-md-summarizer/<run-folder>/`
    - run-folder MUST be: `run-<RUN#>__task-3.2__ref-R19__<YYYYMMDDThhmmssZ>/`

BUNDLE (RUN #20): CODEX_CMD=codex exec --full-auto --skip-git-repo-check --model gpt-5.2 -c model_reasoning_effort=medium | SCOPE: CLI | VALIDATION_BUNDLE: auto_test_openspec/add-xiaoyuzhou-md-summarizer/run-20__task-3.2__ref-R19__20260309T235225Z | HOW_TO_RUN: run.sh/run.bat
EVIDENCE (RUN #20): CODEX_CMD=codex exec --full-auto --skip-git-repo-check --model gpt-5.2 -c model_reasoning_effort=medium | SCOPE: CLI | VALIDATION_BUNDLE: auto_test_openspec/add-xiaoyuzhou-md-summarizer/run-20__task-3.2__ref-R19__20260309T235225Z | WORKER_STARTUP_LOG: auto_test_openspec/add-xiaoyuzhou-md-summarizer/run-20__task-3.2__ref-R19__20260309T235225Z/logs/worker_startup.txt | VALIDATED_CLI: bash run.sh | EXIT_CODE: 0 | RESULT: PASS | GIT_COMMIT: 213b780 | COMMIT_MSG: "Add total timeout cap for API calls (task 3.2, R19)" | DIFFSTAT: "7 files changed, 78 insertions(+), 3 deletions(-)" | FILES: main.py (lines 58,64,78: total_timeout parameter with 300s default), tasks.md, feature_list.json, validation bundle

- [x] 3.3 Fix Whisper model cache memory leak [#R20]
  - ACCEPT: Add explicit model cleanup after transcription completes. Use del + gc.collect() or implement model pooling with size limits.
  - TEST: SCOPE: CLI
    - `python3 -m py_compile main.py` exits with code 0
    - Grep confirms cleanup code is present
    - When done, generate validation bundle under: `auto_test_openspec/add-xiaoyuzhou-md-summarizer/<run-folder>/`
    - run-folder MUST be: `run-<RUN#>__task-3.3__ref-R20__<YYYYMMDDThhmmssZ>/`

BUNDLE (RUN #21): LRU Whisper model cache max=2 + finally cleanup (del model_obj + gc.collect) | VALIDATION_BUNDLE: auto_test_openspec/add-xiaoyuzhou-md-summarizer/run-21__task-3.3__ref-R20__20260309_235741/ | HOW_TO_RUN: run.sh/run.bat
EVIDENCE (RUN #21): CODEX_CMD=codex exec --full-auto --skip-git-repo-check --model gpt-5.2 -c model_reasoning_effort=medium | SCOPE: CLI | VALIDATION_BUNDLE: auto_test_openspec/add-xiaoyuzhou-md-summarizer/run-21__task-3.3__ref-R20__20260309_235741/ | WORKER_STARTUP_LOG: auto_test_openspec/add-xiaoyuzhou-md-summarizer/run-21__task-3.3__ref-R20__20260309_235741/logs/worker_startup.txt | VALIDATED_CLI: python3 -m py_compile main.py && grep "del model_obj" main.py && grep "gc.collect()" main.py && python3 validation check | EXIT_CODE: 0 | RESULT: PASS | GIT_COMMIT: aaeff4d | COMMIT_MSG: "Fix Whisper model cache memory leak (task 3.3, R20)" | DIFFSTAT: "54 files changed, 120 insertions(+), 4 deletions(-)" | FILES: main.py (LRU cache max=2, try/finally cleanup with del+gc.collect), tasks.md, validation bundle

- [ ] 3.4 Fix incomplete temp audio segment cleanup [#R21]
  - ACCEPT: Wrap audio segment processing in try/finally to ensure temp files are always deleted, even on errors.
  - TEST: SCOPE: CLI
    - `python3 -m py_compile main.py` exits with code 0
    - Grep confirms try/finally cleanup pattern
    - When done, generate validation bundle under: `auto_test_openspec/add-xiaoyuzhou-md-summarizer/<run-folder>/`
    - run-folder MUST be: `run-<RUN#>__task-3.4__ref-R21__<YYYYMMDDThhmmssZ>/`

- [ ] 3.5 Fix HTTP retry logic to skip non-retryable errors [#R22]
  - ACCEPT: Modify _retry_with_backoff to check HTTP status codes and skip retrying 4xx errors (only retry 5xx and network errors).
  - TEST: SCOPE: CLI
    - `python3 -m py_compile main.py` exits with code 0
    - Grep confirms status code checking logic
    - When done, generate validation bundle under: `auto_test_openspec/add-xiaoyuzhou-md-summarizer/<run-folder>/`
    - run-folder MUST be: `run-<RUN#>__task-3.5__ref-R22__<YYYYMMDDThhmmssZ>/`
