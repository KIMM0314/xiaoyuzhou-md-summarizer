## ADDED Requirements
### Requirement: Markdown Link Discovery
The system SHALL read a user-provided Markdown file and extract XiaoYuzhou episode links from both Markdown link syntax and plain URLs.

#### Scenario: Extract links from mixed Markdown syntax
- **WHEN** the input Markdown contains XiaoYuzhou URLs in both `[title](url)` and plain URL form
- **THEN** the system returns a deduplicated list of XiaoYuzhou links for processing

### Requirement: Text-First Content Acquisition
The system SHALL attempt to use textual content from each episode page first, and only use audio fallback if extracted text is below a configured threshold.

#### Scenario: Use webpage text when sufficient
- **WHEN** extracted webpage text length is greater than or equal to the minimum text threshold
- **THEN** the system uses webpage text as summarization input without downloading audio

#### Scenario: Fallback to audio when text is insufficient
- **WHEN** extracted webpage text length is below the minimum text threshold
- **THEN** the system attempts to resolve and download a playable audio source for the episode

#### Scenario: Force audio transcription for summarize workflow
- **WHEN** the summarize workflow runs with forced-audio mode enabled (default behavior)
- **THEN** the system skips webpage-text direct use, downloads episode audio, and uses Whisper transcript as summarization input

### Requirement: Local Whisper Transcription
The system SHALL transcribe downloaded episode audio using a local Whisper command and produce a text artifact for downstream summarization.

#### Scenario: Transcribe downloaded audio
- **WHEN** episode audio is successfully downloaded and Whisper command is available
- **THEN** the system generates a local transcript text file and uses it as summarization input

### Requirement: DeepSeek Summary Generation
The system SHALL call a DeepSeek chat-completions API with extracted/transcribed text and return a structured Chinese summary with fixed sections.

#### Scenario: Generate summary from source text
- **WHEN** source text is available and a valid DeepSeek API key is provided
- **THEN** the system returns summary content and persists it to per-episode summary output

#### Scenario: Enforce required summary structure and transcript cleanup
- **WHEN** DeepSeek summary content is generated
- **THEN** the output includes, in order, `# 播客元信息`, `# 播客主要摘要`, `# 主要观点`, `# 支撑观点的例子`, and `# 整理后的原文`
- **AND** the `整理后的原文` section applies light transcript cleanup (sentence cleanup and subheadings) without introducing new facts

### Requirement: Output Persistence
The system SHALL write per-episode outputs and a merged index summary file to a user-specified output directory.

#### Scenario: Save per-episode and merged summaries
- **WHEN** one or more episodes are processed
- **THEN** the system saves each episode summary and writes an aggregated `all_summaries.md` index in the output directory
