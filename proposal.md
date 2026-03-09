# Change: Add XiaoYuzhou Markdown Summarizer CLI

## Why
Users need a local automation workflow to process XiaoYuzhou podcast links stored in Markdown, prioritize text extraction, transcribe audio when needed, and generate readable summaries.

## What Changes
- Add a local CLI tool that reads Markdown and extracts XiaoYuzhou links.
- Add text-first content acquisition with audio fallback.
- Add local Whisper transcription pipeline for downloaded audio.
- Add DeepSeek summarization and save outputs to a user-specified path.
- Enforce a fixed Chinese summary structure: main summary, key viewpoints, supporting examples, and cleaned transcript.
- Require transcript cleanup in the final section (light editing with added subheadings, no fabricated facts).

## Impact
- Affected specs: `podcast-summarizer`
- Affected code: `/Users/langjie/xiaoyuzhou-md-summarizer/main.py`, `/Users/langjie/xiaoyuzhou-md-summarizer/README.md`
