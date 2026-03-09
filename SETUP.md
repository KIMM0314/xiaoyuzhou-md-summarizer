# Setup

## Python

Required: **Python 3.9+**.

Create and activate a virtual environment (recommended):

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 --version
```

Install Python dependencies:

```bash
python3 -m pip install -r requirements.txt
```

Notes:

- `requirements.txt` is intentionally empty because `main.py` uses the Python standard library only.
- If your environment requires `pip` to be upgraded, do so explicitly:
  `python3 -m pip install --upgrade pip`

## DeepSeek configuration (`config.json`)

Summarization uses a JSON config file (default path: `config.json`).

Create it by copying the example:

```bash
cp config.example.json config.json
```

Required fields:

- `deepseek_api_key` (string, required)
- `deepseek_model` (string, required)

Optional CLI overrides (no environment variables required):

- `--deepseek-base-url` (default: `https://api.deepseek.com`)
- `--deepseek-timeout-seconds` (default: `30`)

## Whisper (optional, for audio fallback)

`retrieve-text` and `summarize` will:

- Use webpage text if it is sufficient
- Otherwise, attempt to find an audio URL in the page HTML and run a local Whisper CLI to transcribe it

The CLI expects a command named `whisper` by default (override with `--whisper-cmd`).

Example check:

```bash
whisper --help
```

If Whisper is not installed or not on `PATH`, you can still use the tool when webpage text is sufficient (no audio fallback needed).

## Environment variables

No environment variables are required by default.

- DeepSeek credentials are read from `config.json`.
- Whisper configuration is provided via CLI parameters (`--whisper-cmd`, `--whisper-model`).

