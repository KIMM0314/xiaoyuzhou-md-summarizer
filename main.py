#!/usr/bin/env python3
import argparse
import hashlib
import html.parser
import html as html_lib
import json
import os
import re
import shlex
import subprocess
import sys
import tempfile
import time
from typing import Callable, Optional
from urllib.parse import urlparse
from urllib.request import Request, urlopen


_MARKDOWN_LINK_RE = re.compile(r"\[[^\]]*]\(([^)]+)\)")
_PLAIN_URL_RE = re.compile(r"https?://[^\s<>()]+", re.IGNORECASE)
_TRAILING_PUNCTUATION = ".,;:!?)]}\"'"

_XIAOYUZHOU_DOMAINS = (
    "xiaoyuzhou.com",
    "xiaoyuzhoufm.com",
)

_DEFAULT_HTTP_TIMEOUT_SECONDS = 20
_DEFAULT_USER_AGENT = "Mozilla/5.0 (compatible; xiaoyuzhou-md-summarizer/0.1; +https://example.invalid)"

_DEFAULT_DEEPSEEK_BASE_URL = "https://api.deepseek.com"


def _log(message: str) -> None:
    ts = time.strftime("%H:%M:%S")
    print(f"[{ts}] {message}", file=sys.stderr, flush=True)


def _format_elapsed(start_time: float) -> str:
    elapsed = time.time() - start_time
    minutes = int(elapsed // 60)
    seconds = int(elapsed % 60)
    return f"{minutes}:{seconds:02d}"


def _log_phase(phase: int, total_phases: int, message: str, start_time: float = 0.0) -> None:
    ts = time.strftime("%H:%M:%S")
    elapsed_str = f" | elapsed {_format_elapsed(start_time)}" if start_time > 0 else ""
    print(f"[{ts}] [{phase}/{total_phases}] {message}{elapsed_str}", file=sys.stderr, flush=True)


def _retry_with_backoff(
    operation_name: str,
    action: Callable[[], object],
    *,
    retries: int,
    backoff_seconds: tuple[int, ...],
) -> object:
    total_attempts = max(0, retries) + 1
    last_error: Optional[Exception] = None
    for attempt in range(1, total_attempts + 1):
        try:
            return action()
        except Exception as e:
            last_error = e
            if attempt >= total_attempts:
                break
            delay = backoff_seconds[min(attempt - 1, len(backoff_seconds) - 1)] if backoff_seconds else 0
            _log(f"{operation_name} 失败（第 {attempt}/{total_attempts} 次）: {e}")
            if delay > 0:
                _log(f"{operation_name} 将在 {delay} 秒后重试")
                time.sleep(delay)
    raise RuntimeError(f"{operation_name} 在 {total_attempts} 次尝试后仍失败: {last_error}")


def _normalize_candidate_url(candidate: str) -> str:
    candidate = candidate.strip()
    if candidate.startswith("<") and candidate.endswith(">"):
        candidate = candidate[1:-1].strip()
    candidate = candidate.strip(_TRAILING_PUNCTUATION)
    return candidate


def _extract_markdown_link_urls(markdown_text: str) -> list[str]:
    urls: list[str] = []
    for match in _MARKDOWN_LINK_RE.finditer(markdown_text):
        raw = match.group(1).strip()
        url_part = raw.split()[0] if raw else ""
        url = _normalize_candidate_url(url_part)
        if url:
            urls.append(url)
    return urls


def _extract_plain_urls(markdown_text: str) -> list[str]:
    return [_normalize_candidate_url(m.group(0)) for m in _PLAIN_URL_RE.finditer(markdown_text)]


def _is_xiaoyuzhou_url(url: str) -> bool:
    try:
        parsed = urlparse(url)
    except Exception:
        return False

    if parsed.scheme not in ("http", "https"):
        return False

    host = (parsed.hostname or "").lower().rstrip(".")
    if not host:
        return False

    for domain in _XIAOYUZHOU_DOMAINS:
        if host == domain or host.endswith("." + domain):
            return True
    return False


def extract_links_from_markdown(markdown_text: str) -> list[str]:
    seen: set[str] = set()
    ordered: list[str] = []

    for url in _extract_markdown_link_urls(markdown_text) + _extract_plain_urls(markdown_text):
        if url in seen:
            continue
        seen.add(url)
        ordered.append(url)

    return ordered


class _HTMLTextExtractor(html.parser.HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self._chunks: list[str] = []
        self._ignore_depth = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, Optional[str]]]) -> None:
        tag = tag.lower()
        if tag in ("script", "style", "noscript"):
            self._ignore_depth += 1

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if tag in ("script", "style", "noscript") and self._ignore_depth > 0:
            self._ignore_depth -= 1

    def handle_data(self, data: str) -> None:
        if self._ignore_depth > 0:
            return
        if not data:
            return
        self._chunks.append(data)

    def get_text(self) -> str:
        text = " ".join(self._chunks)
        text = re.sub(r"\s+", " ", text).strip()
        return text


def _read_text_file(path: str) -> str:
    return open(path, "r", encoding="utf-8").read()


def _read_json_file(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, dict):
        raise ValueError("Config JSON must be an object at the top level.")
    return data


def _load_deepseek_config(config_path: str) -> tuple[str, str]:
    try:
        cfg = _read_json_file(config_path)
    except FileNotFoundError:
        raise RuntimeError(f"Config file not found: {config_path}")
    except json.JSONDecodeError as e:
        raise RuntimeError(f"Invalid JSON in config file: {config_path}: {e}")
    except Exception as e:
        raise RuntimeError(f"Failed to read config file: {config_path}: {e}")

    api_key = cfg.get("deepseek_api_key")
    model = cfg.get("deepseek_model")
    if not isinstance(api_key, str) or not api_key.strip():
        raise RuntimeError("Config field deepseek_api_key is required and must be a non-empty string.")
    if not isinstance(model, str) or not model.strip():
        raise RuntimeError("Config field deepseek_model is required and must be a non-empty string.")

    return api_key.strip(), model.strip()


def _deepseek_chat_completions_url(base_url: str) -> str:
    base = (base_url or "").strip().rstrip("/")
    if not base:
        base = _DEFAULT_DEEPSEEK_BASE_URL

    if base.endswith("/v1"):
        return base + "/chat/completions"
    return base + "/v1/chat/completions"


def _deepseek_summarize_markdown(
    text: str,
    *,
    metadata: Optional[dict[str, str]],
    api_key: str,
    model: str,
    base_url: str,
    timeout_seconds: int,
) -> str:
    meta = metadata or {}
    record_date = (meta.get("record_date") or meta.get("publish_date") or "unknown").strip()
    author = (meta.get("author") or "unknown").strip()
    duration = (meta.get("duration") or "unknown").strip()
    title = (meta.get("title") or "unknown").strip()
    episode_url = (meta.get("episode_url") or "unknown").strip()

    if (base_url or "").strip().lower().startswith("stub:"):
        return (
            "# 播客元信息\n\n"
            f"- 录制日期: {record_date}\n"
            f"- 主播/发布者: {author}\n"
            f"- 时长: {duration}\n\n"
            "# 播客主要摘要\n\n"
            "- STUB_SUMMARY_SENTINEL\n\n"
            "# 主要观点\n\n"
            "- （示例）观点 1\n\n"
            "# 支撑观点的例子\n\n"
            "- （示例）例子 1\n\n"
            "# 整理后的原文\n\n"
            "## 小标题示例\n\n"
            "这里是整理后的原文片段。\n\n"
            f"_model: {model}_\n"
            f"_title: {title}_\n"
            f"_url: {episode_url}_\n"
        )

    url = _deepseek_chat_completions_url(base_url)

    user_prompt = (
        "请基于以下播客信息与转写内容，输出中文 Markdown，总共五个一级标题，且顺序必须严格如下：\n"
        "1. # 播客元信息\n"
        "2. # 播客主要摘要\n"
        "3. # 主要观点\n"
        "4. # 支撑观点的例子\n"
        "5. # 整理后的原文\n\n"
        "播客基础信息：\n"
        f"- 标题: {title}\n"
        f"- 链接: {episode_url}\n"
        f"- 录制日期(若未知可用发布日期代替): {record_date}\n"
        f"- 主播/发布者: {author}\n"
        f"- 时长: {duration}\n\n"
        "要求：\n"
        "- 第 1 部分：只包含三条项目符号，依次为“录制日期”“主播/发布者”“时长”；未知则写“未知”。\n"
        "- 第 2 部分：用 3-6 条要点概括整期内容。\n"
        "- 第 3 部分：提炼核心观点，使用项目符号。\n"
        "- 第 4 部分：列出节目中用于支撑观点的具体例子，尽量对应到观点。\n"
        "- 第 5 部分：在不改变原意、不新增事实的前提下，对原文做轻度整理（断句、去口头禅、修正明显错字），并添加合适的小标题（至少 2 个二级标题）。\n"
        "- 只返回 Markdown，不要代码块，不要额外说明。\n\n"
        "以下是原文：\n"
        f"{text}"
    )
    payload = {
        "model": model,
        "temperature": 0.2,
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a precise podcast summarization assistant. "
                    "Follow the user-defined markdown structure exactly."
                ),
            },
            {"role": "user", "content": user_prompt},
        ],
    }

    req = Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "User-Agent": _DEFAULT_USER_AGENT,
        },
        method="POST",
    )

    def _request_once() -> bytes:
        with urlopen(req, timeout=timeout_seconds) as resp:
            return resp.read()

    try:
        raw = _retry_with_backoff(
            "DeepSeek API 请求",
            _request_once,
            retries=3,
            backoff_seconds=(5, 10, 20),
        )
    except Exception as e:
        raise RuntimeError(f"DeepSeek API request failed: {e}")

    if not isinstance(raw, bytes):
        raise RuntimeError("DeepSeek API request returned non-bytes payload.")

    try:
        decoded = json.loads(raw.decode("utf-8", errors="replace"))
    except Exception as e:
        raise RuntimeError(f"DeepSeek API returned invalid JSON: {e}")

    try:
        content = decoded["choices"][0]["message"]["content"]
    except Exception:
        raise RuntimeError("DeepSeek API response missing expected choices[0].message.content.")

    if not isinstance(content, str) or not content.strip():
        raise RuntimeError("DeepSeek API returned empty summary content.")

    return content.strip() + "\n"


def _episode_id_from_url(url: str) -> str:
    try:
        parsed = urlparse(url)
    except Exception:
        parsed = None

    if parsed:
        parts = [p for p in (parsed.path or "").split("/") if p]
        if parts:
            last = parts[-1]
            if re.fullmatch(r"[A-Za-z0-9_-]{6,}", last):
                return last

    h = hashlib.sha256(url.encode("utf-8")).hexdigest()[:12]
    return f"episode_{h}"


def _fetch_url_bytes(url: str, *, timeout_seconds: int = _DEFAULT_HTTP_TIMEOUT_SECONDS) -> tuple[bytes, Optional[str]]:
    parsed = urlparse(url)
    if parsed.scheme == "file":
        file_path = parsed.path
        with open(file_path, "rb") as f:
            return f.read(), None

    req = Request(url, headers={"User-Agent": _DEFAULT_USER_AGENT})
    with urlopen(req, timeout=timeout_seconds) as resp:
        content_type = resp.headers.get("Content-Type")
        return resp.read(), content_type


def _decode_bytes(data: bytes, content_type: Optional[str]) -> str:
    encoding = None
    if content_type:
        m = re.search(r"charset=([^\s;]+)", content_type, re.IGNORECASE)
        if m:
            encoding = m.group(1).strip().strip('"').strip("'")
    try:
        return data.decode(encoding or "utf-8", errors="replace")
    except LookupError:
        return data.decode("utf-8", errors="replace")


def _html_to_text(html: str) -> str:
    parser = _HTMLTextExtractor()
    parser.feed(html)
    return parser.get_text()


_META_TAG_RE = re.compile(r"<meta\s+[^>]*>", re.IGNORECASE)
_META_ATTR_RE = re.compile(r'([A-Za-z_:][A-Za-z0-9_:\-]*)\s*=\s*("([^"]*)"|\'([^\']*)\')', re.IGNORECASE)
_TITLE_TAG_RE = re.compile(r"<title[^>]*>(.*?)</title>", re.IGNORECASE | re.DOTALL)
_PUBLISH_DATE_CANDIDATE_RE = re.compile(
    r"(20\d{2})[-/](\d{1,2})[-/](\d{1,2})(?:[T\s]\d{1,2}:\d{1,2}(?::\d{1,2})?)?",
    re.IGNORECASE,
)
_PUBLISH_KEY_VALUE_RE = re.compile(
    r'"(?:datePublished|publishedAt|publishDate|pubDate|published_time)"\s*:\s*"([^"]+)"',
    re.IGNORECASE,
)
_AUTHOR_KEY_VALUE_RE = re.compile(
    r'"(?:author|uploader|creator|nickname|podcaster|hostName)"\s*:\s*"([^"]+)"',
    re.IGNORECASE,
)
_DURATION_SECONDS_RE = re.compile(
    r'"(?:duration|audioDuration|lengthSeconds)"\s*:\s*"?(\d{1,6})"?',
    re.IGNORECASE,
)
_DURATION_HMS_RE = re.compile(r"\b(\d{1,2}):([0-5]\d)(?::([0-5]\d))?\b")


def _extract_meta_content(html: str, *, prop_names: tuple[str, ...]) -> Optional[str]:
    wanted = {p.lower() for p in prop_names}
    for tag in _META_TAG_RE.findall(html):
        attrs: dict[str, str] = {}
        for m in _META_ATTR_RE.finditer(tag):
            key = m.group(1).lower()
            val = m.group(3) if m.group(3) is not None else (m.group(4) or "")
            attrs[key] = val.strip()
        tag_name = attrs.get("name", "").lower()
        tag_prop = attrs.get("property", "").lower()
        if (tag_name in wanted or tag_prop in wanted) and attrs.get("content", "").strip():
            return html_lib.unescape(attrs["content"].strip())
    return None


def _extract_title_from_html(html: str, episode_url: str) -> str:
    title = _extract_meta_content(
        html,
        prop_names=("og:title", "twitter:title", "title"),
    )
    if title:
        return title

    m = _TITLE_TAG_RE.search(html)
    if m:
        value = re.sub(r"\s+", " ", html_lib.unescape(m.group(1))).strip()
        if value:
            return value

    return _episode_id_from_url(episode_url)


def _normalize_publish_date(raw: str) -> Optional[str]:
    m = _PUBLISH_DATE_CANDIDATE_RE.search(raw)
    if not m:
        return None
    year = int(m.group(1))
    month = int(m.group(2))
    day = int(m.group(3))
    if month < 1 or month > 12 or day < 1 or day > 31:
        return None
    return f"{year:04d}-{month:02d}-{day:02d}"


def _extract_publish_date_from_html(html: str) -> str:
    for m in _PUBLISH_KEY_VALUE_RE.finditer(html):
        date = _normalize_publish_date(m.group(1))
        if date:
            return date

    for candidate in (
        _extract_meta_content(html, prop_names=("article:published_time", "og:published_time", "pubdate", "date")),
        html,
    ):
        if not candidate:
            continue
        date = _normalize_publish_date(candidate)
        if date:
            return date
    return "unknown-date"


def _extract_author_from_html(html: str) -> str:
    author = _extract_meta_content(
        html,
        prop_names=("author", "article:author", "og:audio:artist", "twitter:creator"),
    )
    if author:
        return re.sub(r"\s+", " ", author).strip()

    m = _AUTHOR_KEY_VALUE_RE.search(html)
    if m:
        value = re.sub(r"\s+", " ", html_lib.unescape(m.group(1))).strip()
        if value:
            return value

    return "unknown-author"


def _seconds_to_hms(total_seconds: int) -> str:
    if total_seconds < 0:
        total_seconds = 0
    h, rem = divmod(total_seconds, 3600)
    m, s = divmod(rem, 60)
    if h > 0:
        return f"{h:02d}:{m:02d}:{s:02d}"
    return f"{m:02d}:{s:02d}"


def _extract_duration_from_html(html: str) -> str:
    m = _DURATION_SECONDS_RE.search(html)
    if m:
        try:
            sec = int(m.group(1))
            if sec > 0:
                return _seconds_to_hms(sec)
        except Exception:
            pass

    m = _DURATION_HMS_RE.search(html)
    if m:
        if m.group(3) is None:
            minutes = int(m.group(1))
            seconds = int(m.group(2))
            return _seconds_to_hms(minutes * 60 + seconds)
        hours = int(m.group(1))
        minutes = int(m.group(2))
        seconds = int(m.group(3))
        return _seconds_to_hms(hours * 3600 + minutes * 60 + seconds)

    return "unknown-duration"


def _extract_record_date_from_html(html: str, publish_date: str) -> str:
    for key in ("recordDate", "recordedAt", "record_time", "recorded_time", "create_time"):
        m = re.search(rf'"{key}"\s*:\s*"([^"]+)"', html, re.IGNORECASE)
        if m:
            date = _normalize_publish_date(m.group(1))
            if date:
                return date
    return publish_date


def _render_progress_bar(done: int, total: int, *, width: int = 30) -> str:
    if total <= 0:
        total = 1
    ratio = max(0.0, min(1.0, done / total))
    filled = int(width * ratio)
    return "[" + ("#" * filled) + ("-" * (width - filled)) + f"] {ratio * 100:5.1f}%"


def _print_progress(prefix: str, done: int, total: int) -> None:
    msg = f"\r{prefix} {_render_progress_bar(done, total)} ({done}/{total})"
    print(msg, file=sys.stderr, end="", flush=True)
    if done >= total:
        print("", file=sys.stderr, flush=True)


def _sanitize_filename_component(value: str) -> str:
    cleaned = re.sub(r"[\x00-\x1f]+", "", value).strip()
    cleaned = re.sub(r'[\\/:*?"<>|]+', "_", cleaned)
    cleaned = re.sub(r"\s+", " ", cleaned).strip(" .")
    return cleaned or "untitled"


def _unique_markdown_output_path(output_dir: str, basename: str) -> str:
    candidate = os.path.join(output_dir, basename + ".md")
    if not os.path.exists(candidate):
        return candidate
    idx = 2
    while True:
        candidate = os.path.join(output_dir, f"{basename} ({idx}).md")
        if not os.path.exists(candidate):
            return candidate
        idx += 1


def _find_existing_summary(output_dir: str, basename: str) -> Optional[str]:
    exact = os.path.join(output_dir, basename + ".md")
    if os.path.exists(exact):
        return exact

    if not os.path.isdir(output_dir):
        return None

    pattern = re.compile(rf"^{re.escape(basename)} \((\d+)\)\.md$")
    numbered: list[tuple[int, str]] = []
    for name in os.listdir(output_dir):
        m = pattern.match(name)
        if not m:
            continue
        try:
            idx = int(m.group(1))
        except ValueError:
            continue
        numbered.append((idx, os.path.join(output_dir, name)))
    if not numbered:
        return None
    numbered.sort(key=lambda x: x[0])
    return numbered[0][1]


def _find_existing_summary_for_url(output_dir: str, episode_url: str) -> Optional[str]:
    """
    Best-effort fast skip lookup to avoid expensive download/transcription.

    Strategy:
    1) Parse output_dir/all_summaries.md for URL -> FILE mapping (preferred, O(size of file)).
    2) Fallback: scan the beginning of each .md file for the URL substring.
    """
    if not os.path.isdir(output_dir):
        return None

    index_path = os.path.join(output_dir, "all_summaries.md")
    if os.path.exists(index_path):
        try:
            url_line = f"- URL: {episode_url}".strip()
            file_prefix = "- FILE: "
            with open(index_path, "r", encoding="utf-8") as f:
                pending_match = False
                for raw_line in f:
                    line = (raw_line or "").strip()
                    if pending_match:
                        if line.startswith(file_prefix):
                            filename = line[len(file_prefix) :].strip()
                            if filename:
                                candidate = os.path.join(output_dir, filename)
                                if os.path.exists(candidate):
                                    return candidate
                            pending_match = False
                        elif line.startswith("## ") or line.startswith("- URL: "):
                            pending_match = False
                        continue

                    if line == url_line:
                        pending_match = True
        except OSError:
            pass

    try:
        names = os.listdir(output_dir)
    except OSError:
        return None

    scan_bytes = 16 * 1024
    for name in names:
        if not name.endswith(".md"):
            continue
        if name == "all_summaries.md":
            continue
        path = os.path.join(output_dir, name)
        try:
            with open(path, "rb") as f:
                head = f.read(scan_bytes)
            if episode_url.encode("utf-8") in head:
                return path
        except OSError:
            continue
    return None


def _should_skip_podcast(episode_url: str, output_dir: str, force: bool) -> tuple[bool, Optional[str]]:
    """Check if podcast summary already exists (unless --force)."""
    if force:
        return False, None
    existing = _find_existing_summary_for_url(output_dir, episode_url)
    if existing:
        return True, existing
    return False, None


def _append_to_all_summaries(all_summaries: list[str], *, episode_url: str, summary_path: str) -> None:
    all_summaries.append(f"## {os.path.splitext(os.path.basename(summary_path))[0]}")
    all_summaries.append("")
    all_summaries.append(f"- URL: {episode_url}")
    all_summaries.append(f"- FILE: {os.path.basename(summary_path)}")
    all_summaries.append("")
    try:
        all_summaries.append(_read_text_file(summary_path).rstrip())
    except OSError:
        all_summaries.append("(Failed to read summary file content.)")
    all_summaries.append("")


def _is_text_sufficient(text: str, *, min_words: int, min_chars: int, min_cjk_chars: int) -> bool:
    cleaned = re.sub(r"\s+", " ", text).strip()
    if not cleaned:
        return False

    word_count = len(re.findall(r"[A-Za-z0-9_]+", cleaned))
    nonspace_chars = len(re.sub(r"\s+", "", cleaned))
    cjk_chars = len(re.findall(r"[\u4e00-\u9fff]", cleaned))

    return word_count >= min_words or nonspace_chars >= min_chars or cjk_chars >= min_cjk_chars


_AUDIO_URL_RE = re.compile(
    r"""(?P<url>(?:https?://|file://)[^"'<> \t\r\n]+?\.(?:mp3|m4a|aac|wav|flac)(?:\?[^"'<> \t\r\n]*)?)""",
    re.IGNORECASE,
)


def _find_audio_url_in_html(html: str) -> Optional[str]:
    m = _AUDIO_URL_RE.search(html)
    if m:
        return m.group("url")
    return None


def _safe_filename_from_url(url: str, *, suffix: str) -> str:
    h = hashlib.sha256(url.encode("utf-8")).hexdigest()[:16]
    return f"audio_{h}{suffix}"


def _download_to_file(url: str, dest_path: str) -> None:
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    parsed = urlparse(url)
    chunk_size = 256 * 1024

    if parsed.scheme == "file":
        src = parsed.path
        total = os.path.getsize(src) if os.path.exists(src) else 0
        done = 0
        with open(src, "rb") as rf, open(dest_path, "wb") as wf:
            while True:
                chunk = rf.read(chunk_size)
                if not chunk:
                    break
                wf.write(chunk)
                done += len(chunk)
                if total > 0:
                    _print_progress("[1/3] 下载音频", done, total)
        if total <= 0:
            _log("[1/3] 下载音频完成")
        return

    def _download_http_once() -> None:
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

    try:
        _retry_with_backoff(
            "音频下载",
            _download_http_once,
            retries=2,
            backoff_seconds=(3, 6),
        )
    except Exception:
        try:
            if os.path.exists(dest_path):
                os.remove(dest_path)
        except OSError:
            pass
        raise


_WHISPER_MODEL_CACHE: dict[str, object] = {}


def _probe_audio_duration_seconds(audio_path: str) -> Optional[float]:
    cmd = [
        "ffprobe",
        "-v",
        "error",
        "-show_entries",
        "format=duration",
        "-of",
        "default=noprint_wrappers=1:nokey=1",
        audio_path,
    ]
    try:
        proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=False)
        if proc.returncode != 0:
            return None
        val = (proc.stdout or "").strip()
        if not val:
            return None
        return float(val)
    except Exception:
        return None


def _should_use_python_whisper(whisper_cmd: str) -> bool:
    normalized = " ".join(shlex.split(whisper_cmd.strip())) if whisper_cmd.strip() else ""
    return normalized in {"whisper", "python3 -m whisper", "python -m whisper"}


def _load_whisper_model_cached(model_name: str):
    try:
        import whisper  # type: ignore
    except ImportError:
        raise RuntimeError("Python package 'whisper' is not installed. Please install openai-whisper.")

    if model_name not in _WHISPER_MODEL_CACHE:
        _log(f"加载 Whisper 模型: {model_name}（首次会慢一些）")
        _WHISPER_MODEL_CACHE[model_name] = whisper.load_model(model_name)
    return _WHISPER_MODEL_CACHE[model_name]


def _transcribe_with_python_whisper(audio_path: str, *, output_dir: str, model: str) -> str:
    os.makedirs(output_dir, exist_ok=True)
    base = os.path.splitext(os.path.basename(audio_path))[0]
    transcript_path = os.path.join(output_dir, base + ".txt")
    model_obj = _load_whisper_model_cached(model)

    duration = _probe_audio_duration_seconds(audio_path) or 0.0
    segment_seconds = 600
    segment_paths: list[str] = []
    segment_dir = tempfile.mkdtemp(prefix="xys_segments_", dir=output_dir)

    try:
        if duration > segment_seconds:
            seg_pattern = os.path.join(segment_dir, "seg_%04d.mp3")
            split_cmd = [
                "ffmpeg",
                "-hide_banner",
                "-loglevel",
                "error",
                "-y",
                "-i",
                audio_path,
                "-f",
                "segment",
                "-segment_time",
                str(segment_seconds),
                "-c",
                "copy",
                seg_pattern,
            ]
            split_proc = subprocess.run(split_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=False)
            if split_proc.returncode == 0:
                segment_paths = sorted(
                    os.path.join(segment_dir, n)
                    for n in os.listdir(segment_dir)
                    if n.endswith(".mp3")
                )

        if not segment_paths:
            segment_paths = [audio_path]

        texts: list[str] = []
        total = len(segment_paths)
        _log(f"Whisper 转写分段数: {total}")
        transcribe_started_at = time.time()
        for idx, seg_path in enumerate(segment_paths, start=1):
            result = model_obj.transcribe(
                seg_path,
                fp16=False,
                verbose=False,
            )
            chunk_text = (result.get("text") or "").strip()
            if chunk_text:
                texts.append(chunk_text)
            _print_progress(f"[2/3] 转写进度 | elapsed {_format_elapsed(transcribe_started_at)}", idx, total)

        transcript_text = "\n".join(t for t in texts if t).strip()
        if not transcript_text:
            raise RuntimeError("Whisper produced empty transcript text.")

        with open(transcript_path, "w", encoding="utf-8") as f:
            f.write(transcript_text)
        _log(f"Whisper 转写完成，输出={transcript_path}")
        return transcript_text
    finally:
        for p in segment_paths:
            if p.startswith(segment_dir):
                try:
                    os.remove(p)
                except OSError:
                    pass
        try:
            os.rmdir(segment_dir)
        except OSError:
            pass


def _run_whisper(
    whisper_cmd: str,
    *,
    audio_path: str,
    output_dir: str,
    model: str,
) -> str:
    os.makedirs(output_dir, exist_ok=True)
    if _should_use_python_whisper(whisper_cmd):
        return _transcribe_with_python_whisper(audio_path, output_dir=output_dir, model=model)

    base_cmd = shlex.split(whisper_cmd) if whisper_cmd.strip() else []
    if not base_cmd:
        raise RuntimeError("Whisper command is empty.")

    cmd = [
        *base_cmd,
        audio_path,
        "--model",
        model,
        "--output_dir",
        output_dir,
        "--output_format",
        "txt",
    ]
    _log(f"Whisper 外部命令转写: {' '.join(cmd)}")
    try:
        proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=False)
    except FileNotFoundError:
        raise RuntimeError(f"Whisper command not found: {whisper_cmd}")

    if proc.returncode != 0:
        stderr = (proc.stderr or "").strip()
        stdout = (proc.stdout or "").strip()
        details = "\n".join([s for s in (stderr, stdout) if s])
        raise RuntimeError(f"Whisper failed (exit={proc.returncode}). {details}".strip())

    base = os.path.splitext(os.path.basename(audio_path))[0]
    transcript_path = os.path.join(output_dir, base + ".txt")
    try:
        text = _read_text_file(transcript_path).strip()
        _log(f"Whisper 转写完成，输出={transcript_path}")
        return text
    except FileNotFoundError:
        raise RuntimeError(f"Whisper did not produce expected transcript file: {transcript_path}")


def retrieve_text_with_audio_fallback(
    episode_url: str,
    *,
    min_words: int,
    min_chars: int,
    min_cjk_chars: int,
    whisper_cmd: str,
    whisper_model: str,
    work_dir: str,
    force_audio_transcription: bool = False,
) -> tuple[str, str, dict[str, str]]:
    _log(f"开始抓取页面: {episode_url}")
    page_bytes, content_type = _fetch_url_bytes(episode_url)
    html = _decode_bytes(page_bytes, content_type)
    page_text = _html_to_text(html)
    publish_date = _extract_publish_date_from_html(html)
    metadata = {
        "title": _extract_title_from_html(html, episode_url),
        "publish_date": publish_date,
        "record_date": _extract_record_date_from_html(html, publish_date),
        "author": _extract_author_from_html(html),
        "duration": _extract_duration_from_html(html),
        "episode_url": episode_url,
    }

    if (not force_audio_transcription) and _is_text_sufficient(
        page_text,
        min_words=min_words,
        min_chars=min_chars,
        min_cjk_chars=min_cjk_chars,
    ):
        _log("网页文本已达阈值，跳过音频下载与转写")
        return "web_text", page_text, metadata

    audio_url = _find_audio_url_in_html(html)
    if not audio_url:
        if force_audio_transcription:
            raise RuntimeError("Force-audio mode enabled but no audio URL found in HTML.")
        raise RuntimeError("Webpage text insufficient and no audio URL found in HTML.")

    _log("开始下载音频")
    parsed_audio = urlparse(audio_url)
    suffix = os.path.splitext(parsed_audio.path)[1] or ".mp3"
    audio_path = os.path.join(work_dir, _safe_filename_from_url(audio_url, suffix=suffix))
    _download_to_file(audio_url, audio_path)
    _log(f"音频下载完成: {audio_path}")

    transcript_dir = os.path.join(work_dir, "whisper_out")
    _log("开始 Whisper 转写（这一步可能较慢，请等待）")
    transcript_text = _run_whisper(
        whisper_cmd,
        audio_path=audio_path,
        output_dir=transcript_dir,
        model=whisper_model,
    )
    return "whisper_transcript", transcript_text, metadata


def _legacy_extract_links(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Extract XiaoYuzhou links from a Markdown file.")
    parser.add_argument("--md-file", required=True, help="Path to Markdown file to scan for links.")
    args = parser.parse_args(argv)

    try:
        markdown_text = _read_text_file(args.md_file)
    except FileNotFoundError:
        print(f"ERROR: Markdown file not found: {args.md_file}", file=sys.stderr)
        return 2
    except OSError as e:
        print(f"ERROR: Failed to read Markdown file: {args.md_file}: {e}", file=sys.stderr)
        return 2

    filtered = [url for url in extract_links_from_markdown(markdown_text) if _is_xiaoyuzhou_url(url)]
    for url in filtered:
        print(url)
    return 0


def main(argv: list[str]) -> int:
    if not argv or argv[0] not in ("extract-links", "retrieve-text", "summarize"):
        return _legacy_extract_links(argv)

    parser = argparse.ArgumentParser(prog=f"{os.path.basename(sys.argv[0])} {argv[0]}")
    subparsers = parser.add_subparsers(dest="cmd", required=True)

    extract_parser = subparsers.add_parser("extract-links", help="Extract XiaoYuzhou links from Markdown.")
    extract_parser.add_argument("--md-file", required=True, help="Path to Markdown file to scan for links.")

    retrieve_parser = subparsers.add_parser(
        "retrieve-text",
        help="Retrieve episode text; if insufficient, download audio and transcribe via local Whisper CLI.",
    )
    retrieve_parser.add_argument("--md-file", help="Optional Markdown file to scan for episode links.")
    retrieve_parser.add_argument("--url", action="append", default=[], help="Episode URL to retrieve (repeatable).")
    retrieve_parser.add_argument(
        "--only-xiaoyuzhou",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="When using --md-file, keep only XiaoYuzhou links (default: true).",
    )
    retrieve_parser.add_argument("--min-words", type=int, default=80, help="Web text sufficiency threshold (word count).")
    retrieve_parser.add_argument(
        "--min-chars",
        type=int,
        default=400,
        help="Web text sufficiency threshold (non-space character count).",
    )
    retrieve_parser.add_argument(
        "--min-cjk-chars",
        type=int,
        default=200,
        help="Web text sufficiency threshold (CJK character count).",
    )
    retrieve_parser.add_argument(
        "--whisper-cmd",
        default="whisper",
        help="Whisper CLI command (default: whisper).",
    )
    retrieve_parser.add_argument(
        "--whisper-model",
        default="tiny",
        help="Whisper model name (default: tiny).",
    )
    retrieve_parser.add_argument(
        "--work-dir",
        default="",
        help="Directory for downloaded audio and transcripts (default: temp dir).",
    )
    retrieve_parser.add_argument(
        "--output-file",
        default="",
        help="Optional output file path (default: write to stdout).",
    )
    retrieve_parser.add_argument(
        "--force-audio-transcription",
        action=argparse.BooleanOptionalAction,
        default=False,
        help="Always download audio and transcribe with Whisper, skipping webpage-text direct use (default: false).",
    )

    summarize_parser = subparsers.add_parser(
        "summarize",
        help="Retrieve episode text and summarize via DeepSeek; write per-episode and aggregated Markdown outputs.",
    )
    summarize_parser.add_argument("--md-file", help="Optional Markdown file to scan for episode links.")
    summarize_parser.add_argument("--url", action="append", default=[], help="Episode URL to summarize (repeatable).")
    summarize_parser.add_argument(
        "--only-xiaoyuzhou",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="When using --md-file, keep only XiaoYuzhou links (default: true).",
    )
    summarize_parser.add_argument("--min-words", type=int, default=80, help="Web text sufficiency threshold (word count).")
    summarize_parser.add_argument(
        "--min-chars",
        type=int,
        default=400,
        help="Web text sufficiency threshold (non-space character count).",
    )
    summarize_parser.add_argument(
        "--min-cjk-chars",
        type=int,
        default=200,
        help="Web text sufficiency threshold (CJK character count).",
    )
    summarize_parser.add_argument(
        "--whisper-cmd",
        default="whisper",
        help="Whisper CLI command (default: whisper).",
    )
    summarize_parser.add_argument(
        "--whisper-model",
        default="tiny",
        help="Whisper model name (default: tiny).",
    )
    summarize_parser.add_argument(
        "--work-dir",
        default="",
        help="Directory for downloaded audio and transcripts (default: temp dir).",
    )
    summarize_parser.add_argument(
        "--config",
        default="config.json",
        help="Path to config.json containing DeepSeek credentials (default: config.json).",
    )
    summarize_parser.add_argument(
        "--deepseek-base-url",
        default=_DEFAULT_DEEPSEEK_BASE_URL,
        help=f"DeepSeek API base URL (default: {_DEFAULT_DEEPSEEK_BASE_URL}).",
    )
    summarize_parser.add_argument(
        "--deepseek-timeout-seconds",
        type=int,
        default=120,
        help="DeepSeek request timeout in seconds (default: 120).",
    )
    summarize_parser.add_argument(
        "--force-audio-transcription",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Always download audio and transcribe with Whisper before summarization (default: true).",
    )
    summarize_parser.add_argument(
        "--output-dir",
        required=True,
        help="Target directory to write <publish_date>_<title>.md files and all_summaries.md.",
    )
    summarize_parser.add_argument(
        "--force",
        action=argparse.BooleanOptionalAction,
        default=False,
        help="Force re-processing even when summary output already exists (default: false).",
    )

    args = parser.parse_args(argv)

    if args.cmd == "extract-links":
        return _legacy_extract_links(["--md-file", args.md_file])

    if args.cmd == "summarize":
        urls: list[str] = []
        for u in args.url:
            u = _normalize_candidate_url(u)
            if u:
                urls.append(u)

        if args.md_file:
            try:
                markdown_text = _read_text_file(args.md_file)
            except FileNotFoundError:
                print(f"ERROR: Markdown file not found: {args.md_file}", file=sys.stderr)
                return 2
            except OSError as e:
                print(f"ERROR: Failed to read Markdown file: {args.md_file}: {e}", file=sys.stderr)
                return 2

            extracted = extract_links_from_markdown(markdown_text)
            if args.only_xiaoyuzhou:
                extracted = [u for u in extracted if _is_xiaoyuzhou_url(u)]
            urls.extend(extracted)

        deduped: list[str] = []
        seen: set[str] = set()
        for u in urls:
            if u in seen:
                continue
            seen.add(u)
            deduped.append(u)

        if not deduped:
            print("ERROR: No URLs to summarize. Provide --url and/or --md-file.", file=sys.stderr)
            return 2

        try:
            api_key, model = _load_deepseek_config(args.config)
        except Exception as e:
            print(f"ERROR: {e}", file=sys.stderr)
            return 2

        work_dir = args.work_dir.strip()
        temp_dir_obj: Optional[tempfile.TemporaryDirectory] = None
        if not work_dir:
            temp_dir_obj = tempfile.TemporaryDirectory(prefix="xys_summarize_")
            work_dir = temp_dir_obj.name
        else:
            os.makedirs(work_dir, exist_ok=True)

        os.makedirs(args.output_dir, exist_ok=True)
        all_summaries: list[str] = ["# All episode summaries", ""]
        total = len(deduped)
        _log(f"准备处理 {total} 个播客链接")
        success_count = 0
        failure_count = 0
        skipped_count = 0
        failures: list[tuple[str, str]] = []

        for idx, episode_url in enumerate(deduped, start=1):
            episode_started_at = time.time()
            _log("=" * 72)
            _log(f"Podcast {idx}/{total}")
            _log(f"URL: {episode_url}")

            should_skip, existing_file = _should_skip_podcast(episode_url, args.output_dir, bool(args.force))
            if should_skip and existing_file:
                skipped_count += 1
                _log_phase(
                    1,
                    3,
                    f"已存在摘要，跳过（可用 --force 覆盖）: {existing_file}",
                    start_time=episode_started_at,
                )
                _append_to_all_summaries(all_summaries, episode_url=episode_url, summary_path=existing_file)
                continue
            try:
                _log_phase(1, 3, "开始获取播客内容")
                source, source_text, metadata = retrieve_text_with_audio_fallback(
                    episode_url,
                    min_words=args.min_words,
                    min_chars=args.min_chars,
                    min_cjk_chars=args.min_cjk_chars,
                    whisper_cmd=args.whisper_cmd,
                    whisper_model=args.whisper_model,
                    work_dir=work_dir,
                    force_audio_transcription=bool(args.force_audio_transcription),
                )
                _log_phase(1, 3, f"获取完成，来源={source}", start_time=episode_started_at)
            except Exception as e:
                failure_count += 1
                failures.append((episode_url, f"retrieve failed: {e}"))
                print(f"ERROR: Failed to retrieve {episode_url}: {e}", file=sys.stderr)
                continue

            publish_date = _sanitize_filename_component(metadata.get("publish_date", "unknown-date"))
            title = _sanitize_filename_component(metadata.get("title", _episode_id_from_url(episode_url)))
            summary_basename = f"{publish_date}_{title}"
            existing_summary = _find_existing_summary(args.output_dir, summary_basename)
            if existing_summary and not args.force:
                skipped_count += 1
                _log_phase(3, 3, f"已存在摘要，跳过（可用 --force 覆盖）: {existing_summary}", start_time=episode_started_at)
                _append_to_all_summaries(all_summaries, episode_url=episode_url, summary_path=existing_summary)
                continue

            try:
                _log_phase(3, 3, "开始调用 DeepSeek 总结")
                summary_md = _deepseek_summarize_markdown(
                    source_text.strip(),
                    metadata=metadata,
                    api_key=api_key,
                    model=model,
                    base_url=args.deepseek_base_url,
                    timeout_seconds=max(1, int(args.deepseek_timeout_seconds)),
                )
                _log_phase(3, 3, "DeepSeek 返回完成", start_time=episode_started_at)
            except Exception as e:
                failure_count += 1
                failures.append((episode_url, f"summarize failed: {e}"))
                print(f"ERROR: DeepSeek summarization failed for {episode_url}: {e}", file=sys.stderr)
                continue

            summary_path = _unique_markdown_output_path(args.output_dir, summary_basename)
            with open(summary_path, "w", encoding="utf-8") as f:
                f.write(summary_md)
            success_count += 1
            _log_phase(3, 3, f"已写入: {summary_path}", start_time=episode_started_at)
            _append_to_all_summaries(all_summaries, episode_url=episode_url, summary_path=summary_path)

        with open(os.path.join(args.output_dir, "all_summaries.md"), "w", encoding="utf-8") as f:
            f.write("\n".join(all_summaries).rstrip() + "\n")
        _log("已写入汇总文件: all_summaries.md")
        _log(f"处理结果汇总: success={success_count}, failed={failure_count}, skipped={skipped_count}")
        if failures:
            _log("失败条目明细:")
            for failed_url, reason in failures:
                _log(f"- {failed_url}: {reason}")

        if temp_dir_obj is not None:
            temp_dir_obj.cleanup()

        if failure_count > 0:
            return 5
        return 0

    urls: list[str] = []
    for u in args.url:
        u = _normalize_candidate_url(u)
        if u:
            urls.append(u)

    if args.md_file:
        try:
            markdown_text = _read_text_file(args.md_file)
        except FileNotFoundError:
            print(f"ERROR: Markdown file not found: {args.md_file}", file=sys.stderr)
            return 2
        except OSError as e:
            print(f"ERROR: Failed to read Markdown file: {args.md_file}: {e}", file=sys.stderr)
            return 2

        extracted = extract_links_from_markdown(markdown_text)
        if args.only_xiaoyuzhou:
            extracted = [u for u in extracted if _is_xiaoyuzhou_url(u)]
        urls.extend(extracted)

    deduped: list[str] = []
    seen: set[str] = set()
    for u in urls:
        if u in seen:
            continue
        seen.add(u)
        deduped.append(u)

    if not deduped:
        print("ERROR: No URLs to retrieve. Provide --url and/or --md-file.", file=sys.stderr)
        return 2

    work_dir = args.work_dir.strip()
    temp_dir_obj: Optional[tempfile.TemporaryDirectory] = None
    if not work_dir:
        temp_dir_obj = tempfile.TemporaryDirectory(prefix="xys_retrieve_")
        work_dir = temp_dir_obj.name
    else:
        os.makedirs(work_dir, exist_ok=True)

    output_chunks: list[str] = []
    for episode_url in deduped:
        try:
            source, text, _ = retrieve_text_with_audio_fallback(
                episode_url,
                min_words=args.min_words,
                min_chars=args.min_chars,
                min_cjk_chars=args.min_cjk_chars,
                whisper_cmd=args.whisper_cmd,
                whisper_model=args.whisper_model,
                work_dir=work_dir,
                force_audio_transcription=bool(args.force_audio_transcription),
            )
        except Exception as e:
            print(f"ERROR: Failed to retrieve {episode_url}: {e}", file=sys.stderr)
            return 3

        output_chunks.append("=== BEGIN EPISODE ===")
        output_chunks.append(f"URL: {episode_url}")
        output_chunks.append(f"SOURCE: {source}")
        output_chunks.append("TEXT:")
        output_chunks.append(text.strip())
        output_chunks.append("=== END EPISODE ===")

    output = "\n".join(output_chunks).rstrip() + "\n"
    if args.output_file:
        os.makedirs(os.path.dirname(args.output_file) or ".", exist_ok=True)
        with open(args.output_file, "w", encoding="utf-8") as f:
            f.write(output)
    else:
        sys.stdout.write(output)

    if temp_dir_obj is not None:
        temp_dir_obj.cleanup()

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
