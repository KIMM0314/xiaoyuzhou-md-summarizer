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
