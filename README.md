# XiaoYuzhou Markdown Summarizer (CLI)

This repository provides a small Python CLI that:

- Extracts XiaoYuzhou episode links from a Markdown file
- Retrieves episode text (webpage text first; audio+Whisper fallback if needed)
- Summarizes retrieved text via DeepSeek and writes Markdown outputs (audio transcription is forced by default in `summarize`)
  - Summary format is fixed to: main summary, key viewpoints, supporting examples, and cleaned transcript with subheadings

## Requirements

- Python **3.9+** (recommended: 3.11+)
- **Optional (only for audio fallback):** a working `whisper` CLI on your `PATH` (see `SETUP.md`)
- **For summarization:** `config.json` with DeepSeek credentials (see `config.example.json`)

Runtime Python dependencies: **stdlib only** (see `requirements.txt`).

## Quick start

1) Create a `config.json` (copy and edit):

- Copy `config.example.json` → `config.json`
- Set:
  - `deepseek_api_key`
  - `deepseek_model`

2) Run a basic summarize workflow:

```bash
python3 main.py summarize \
  --url "https://www.xiaoyuzhoufm.com/episode/EPISODE_ID" \
  --config config.json \
  --output-dir outputs/summaries
```

Outputs:

- `outputs/summaries/<publish_date>_<title>.md`
- `outputs/summaries/all_summaries.md`

## Documentation

- Setup: `SETUP.md`
- Usage examples: `USAGE.md`
