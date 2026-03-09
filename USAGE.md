# CLI Usage

All commands are run from the repository directory.

## 1) Extract XiaoYuzhou links from Markdown

Legacy mode (kept for backward compatibility):

```bash
python3 main.py --md-file inputs/sample.md
```

Explicit subcommand:

```bash
python3 main.py extract-links --md-file inputs/sample.md
```

## 2) Retrieve episode text (web first, audio fallback)

Retrieve directly from a URL:

```bash
python3 main.py retrieve-text \
  --url "https://www.xiaoyuzhoufm.com/episode/EPISODE_ID"
```

Retrieve from a Markdown file containing links:

```bash
python3 main.py retrieve-text \
  --md-file inputs/sample.md \
  --only-xiaoyuzhou
```

Write retrieval output to a file:

```bash
python3 main.py retrieve-text \
  --url "https://www.xiaoyuzhoufm.com/episode/EPISODE_ID" \
  --output-file outputs/retrieval.txt
```

Whisper controls (only used if the webpage text is insufficient):

```bash
python3 main.py retrieve-text \
  --url "https://www.xiaoyuzhoufm.com/episode/EPISODE_ID" \
  --whisper-cmd "whisper" \
  --whisper-model "tiny" \
  --work-dir outputs/work
```

## 3) Summarize via DeepSeek

Prepare `config.json`:

- Copy `config.example.json` → `config.json`
- Set `deepseek_api_key` and `deepseek_model`

Summarize a single episode URL:

```bash
python3 main.py summarize \
  --url "https://www.xiaoyuzhoufm.com/episode/EPISODE_ID" \
  --config config.json \
  --output-dir outputs/summaries
```

Note: `summarize` now defaults to `--force-audio-transcription`, so it will download audio and run local Whisper before calling DeepSeek.

Summarize from links found in a Markdown file:

```bash
python3 main.py summarize \
  --md-file inputs/sample.md \
  --only-xiaoyuzhou \
  --force-audio-transcription \
  --config config.json \
  --output-dir outputs/summaries
```

### Offline / deterministic test mode

The CLI supports a stubbed DeepSeek base URL for deterministic runs:

```bash
python3 main.py summarize \
  --url "file://$(pwd)/inputs/fixtures/episode.html" \
  --config config.json \
  --deepseek-base-url "stub:" \
  --output-dir outputs/summaries
```

When `--deepseek-base-url` starts with `stub:`, the program does not make a network request and produces a stub summary.

## Output structure

For `summarize --output-dir <DIR>`:

- `<DIR>/<publish_date>_<title>.md`
- `<DIR>/all_summaries.md`

Each `summary.md` is instructed to follow this section order:

1. `# 播客元信息`
2. `# 播客主要摘要`
3. `# 主要观点`
4. `# 支撑观点的例子`
5. `# 整理后的原文` (with added subheadings and light transcript cleanup)

If publish date/title are unavailable, filename falls back to `unknown-date_<episode_id>.md`.

## Troubleshooting

- `ERROR: Config file not found: config.json`
  - Provide `--config /path/to/config.json` or create `config.json` from `config.example.json`.
- `ERROR: Whisper command not found: whisper`
  - Install Whisper or set `--whisper-cmd` to the correct executable path.
- Retrieval fails on `https://...` in restricted environments
  - Use `file://...` fixtures and `--deepseek-base-url stub:` for offline testing.
