#!/usr/bin/env python3
"""Static site generator for discrete-math-from-scratch.

Walks phases/**/NN-lesson-name/docs/en.md, reads YAML-lite front-matter
(title, type, prerequisites, time), converts the lesson markdown to HTML
with a small built-in renderer, and writes:

    site/index.html          catalog grouped by phase
    site/lesson/<name>.html  one page per lesson
    site/style.css           stylesheet

Zero dependencies. Python 3.10+.
"""

from __future__ import annotations

import html
import json
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PHASES_DIR = ROOT / "phases"
SITE_DIR = ROOT / "site"

FRONT_MATTER_RE = re.compile(r"\A---\s*\n(.*?)\n---\s*\n", re.DOTALL)

PRE_POOL_SIZE = 5
PRE_SHOWN = 3
POST_POOL_SIZE = 6
POST_SHOWN = 4


def load_quiz(lesson_dir: Path) -> dict:
    quiz_path = lesson_dir / "quiz.json"
    if not quiz_path.exists():
        return {}
    try:
        data = json.loads(quiz_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        print(f"WARNING: bad quiz.json in {lesson_dir.name}: {exc}")
        return {}
    pools: dict[str, list] = {"pre": [], "post": []}
    for q in data.get("questions", []):
        stage = q.get("stage")
        if stage in pools:
            pools[stage].append(q)
    return pools


def embed_quiz_data(pools: dict) -> str:
    if not pools:
        return ""
    payload = {
        "pre": {"pool": pools["pre"], "shown": PRE_SHOWN},
        "post": {"pool": pools["post"], "shown": POST_SHOWN},
    }
    return (
        '<script id="quiz-data" type="application/json">'
        + json.dumps(payload).replace("</", "<\\/")
        + "</script>"
    )


def parse_front_matter(text: str) -> tuple[dict, str]:
    match = FRONT_MATTER_RE.match(text)
    meta: dict = {}
    body = text
    if match:
        body = text[match.end():]
        for line in match.group(1).splitlines():
            if ":" not in line:
                continue
            key, _, raw = line.partition(":")
            raw = raw.strip()
            if raw.startswith("[") and raw.endswith("]"):
                items = [item.strip().strip("'\"") for item in raw[1:-1].split(",") if item.strip()]
                meta[key.strip()] = items
            else:
                meta[key.strip()] = raw
    return meta, body


def slugify(text: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return slug or "section"


def inline_md(text: str) -> str:
    text = html.escape(text, quote=False)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<!\*)\*([^*]+?)\*(?!\*)", r"<em>\1</em>", text)
    text = re.sub(r"`([^`]+?)`", r"<code>\1</code>", text)
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', text)
    return text


def insert_quiz_mounts(lesson_html: str, pools: dict) -> str:
    if not pools:
        return lesson_html

    def mount(kind: str, title: str, blurb: str) -> str:
        shown = PRE_SHOWN if kind == "pre" else POST_SHOWN
        return (
            f'<div class="quiz-mount" data-quiz="{kind}" data-title="{title}">'
            f"<p class=\"quiz-blurb\">{blurb} "
            f"{shown} questions are drawn at random from a larger pool — "
            "reload for a different set.</p></div>"
        )

    html_out = lesson_html
    pre_mount = mount(
        "pre", "Pre-Lesson Check",
        "Answer before reading. They show what to skim first.",
    )
    post_mount = mount(
        "post", "Test Your Understanding",
        "Answer after working through the lesson.",
    )
    html_out, n_pre = re.subn(
        r'<h2 id="pre-lesson-check">.*?</h2>',
        lambda m: m.group(0) + pre_mount,
        html_out, count=1,
    )
    html_out, n_post = re.subn(
        r'<h2 id="test-your-understanding">.*?</h2>',
        lambda m: m.group(0) + post_mount,
        html_out, count=1,
    )
    if n_pre == 0 or n_post == 0:
        print("WARNING: lesson missing Pre-Lesson Check or Test Your Understanding heading")
    return html_out


def render_markdown(body: str) -> str:
    lines = body.splitlines()
    out: list[str] = []
    para: list[str] = []
    in_code = False
    code: list[str] = []
    table: list[list[str]] = []
    in_list = False
    list_tag = "ul"

    def flush_para() -> None:
        nonlocal para
        if para:
            out.append("<p>" + inline_md(" ".join(para)) + "</p>")
            para = []

    def flush_table() -> None:
        nonlocal table
        if not table:
            return
        rows = [r for r in table if not all(re.fullmatch(r":?-+:?", c) for c in r)]
        html_rows = []
        for i, row in enumerate(rows):
            tag = "th" if i == 0 else "td"
            cells = "".join(f"<{tag}>{inline_md(c)}</{tag}>" for c in row)
            html_rows.append(f"<tr>{cells}</tr>")
        out.append("<table>" + "".join(html_rows) + "</table>")
        table = []

    def flush_list() -> None:
        nonlocal in_list
        if in_list:
            out.append(f"</{list_tag}>")
            in_list = False

    for line in lines:
        if line.strip().startswith("```"):
            if in_code:
                out.append('<pre><code class="lang-python">' + html.escape("\n".join(code)) + "</code></pre>")
                code = []
                in_code = False
            else:
                flush_para()
                flush_table()
                flush_list()
                in_code = True
            continue
        if in_code:
            code.append(line)
            continue
        stripped = line.strip()
        if stripped.startswith("|") and stripped.endswith("|"):
            flush_para()
            flush_list()
            cells = [c.strip() for c in stripped.strip("|").split("|")]
            table.append(cells)
            continue
        flush_table()
        if stripped.startswith("> "):
            flush_para()
            flush_list()
            out.append("<blockquote>" + inline_md(stripped[2:]) + "</blockquote>")
            continue
        heading = re.match(r"^(#{1,4})\s+(.*)$", stripped)
        if heading:
            flush_para()
            flush_list()
            level = len(heading.group(1))
            text = heading.group(2)
            if level in (2, 3):
                out.append(f'<h{level} id="{slugify(text)}">{inline_md(text)}</h{level}>')
            else:
                out.append(f"<h{level}>{inline_md(text)}</h{level}>")
            continue
        if stripped == "":
            flush_para()
            flush_list()
            continue
        if stripped == "---":
            flush_para()
            flush_list()
            out.append("<hr>")
            continue
        bullet = re.match(r"^[-*]\s+(.*)$", stripped)
        numbered = re.match(r"^\d+\.\s+(.*)$", stripped)
        if bullet or numbered:
            flush_para()
            tag = "ul" if bullet else "ol"
            if not in_list or list_tag != tag:
                if in_list:
                    out.append(f"</{list_tag}>")
                out.append(f"<{tag}>")
                in_list = True
                list_tag = tag
            out.append("<li>" + inline_md((bullet or numbered).group(1)) + "</li>")
            continue
        flush_list()
        para.append(stripped)
    flush_para()
    flush_table()
    flush_list()
    return "\n".join(out)


def discover_lessons() -> list[dict]:
    lessons: list[dict] = []
    if not PHASES_DIR.exists():
        return lessons
    for phase_dir in sorted(PHASES_DIR.iterdir()):
        if not phase_dir.is_dir():
            continue
        for lesson_dir in sorted(phase_dir.iterdir()):
            doc = lesson_dir / "docs" / "en.md"
            if not doc.exists():
                continue
            meta, body = parse_front_matter(doc.read_text(encoding="utf-8"))
            slug = lesson_dir.name
            pools = load_quiz(lesson_dir)
            lesson_html = insert_quiz_mounts(render_markdown(body), pools)
            lessons.append({
                "slug": slug,
                "phase_dir": phase_dir.name,
                "phase_num": phase_dir.name.split("-", 1)[0],
                "phase_name": phase_dir.name.split("-", 1)[1].replace("-", " ").title(),
                "title": meta.get("title", slug),
                "type": meta.get("type", "Build"),
                "prerequisites": meta.get("prerequisites", []),
                "time": meta.get("time", "?"),
                "html": lesson_html,
                "quiz_data": embed_quiz_data(pools),
            })
    return lessons


PAGE_SHELL = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} · discrete math from scratch</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=VT323&family=Source+Serif+4:ital,opsz,wght@0,8..60,400..700;1,8..60,400&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{css}">
</head>
<body>
{sidebar}
<div class="layout">
<main>
{content}
</main>
{toc}
</div>
<footer>
<p><a href="https://github.com/Barzin/discrete-math-from-scratch">Source on GitHub</a> ·
Inspired by <a href="https://github.com/rohitg00/ai-engineering-from-scratch">ai-engineering-from-scratch</a> · MIT</p>
</footer>
</body>
</html>
"""


def render_sidebar(lessons: list[dict], home: str) -> str:
    groups: dict[str, list[dict]] = {}
    for lesson in lessons:
        groups.setdefault(lesson["phase_dir"], []).append(lesson)
    parts = [
        '<aside class="sidebar"><p class="side-brand">'
        f'<a href="{home}">discrete-math-from-scratch</a></p>'
    ]
    for phase_dir, group in groups.items():
        num, name = phase_dir.split("-", 1)
        parts.append(
            f'<p class="side-phase">{num} · {html.escape(name.replace("-", " ").title())}</p>'
        )
        for lesson in group:
            href = home.replace("index.html", f"lesson/{lesson['slug']}.html")
            current = " class=\"current\"" if lesson.get("current") else ""
            parts.append(f'<p class="side-lesson"><a{current} href="{href}">'
                         f'{html.escape(lesson["title"])}</a></p>')
    parts.append("</aside>")
    return "".join(parts)


def render_toc(lesson_html: str) -> str:
    headings = re.findall(r'<h2 id="([^"]+)">(.*?)</h2>', lesson_html)
    if not headings:
        return ""
    items = "".join(f'<li><a href="#{hid}">{re.sub(r"<[^>]+>", "", t)}</a></li>'
                    for hid, t in headings)
    return f'<aside class="toc"><p class="toc-title">On this page</p><ul>{items}</ul></aside>'


def build(lessons: list[dict]) -> None:
    if SITE_DIR.exists():
        shutil.rmtree(SITE_DIR)
    (SITE_DIR / "lesson").mkdir(parents=True)
    shutil.copy(ROOT / "tools" / "style.css", SITE_DIR / "style.css")
    shutil.copy(ROOT / "tools" / "quiz.js", SITE_DIR / "quiz.js")

    phases: dict[str, list[dict]] = {}
    for lesson in lessons:
        phases.setdefault(lesson["phase_dir"], []).append(lesson)

    phase_rows = []
    for phase_dir, group in phases.items():
        rows = "".join(
            f'<tr><td class="num">{l["slug"].split("-", 1)[0]}</td>'
            f'<td><a href="lesson/{l["slug"]}.html">{html.escape(l["title"])}</a></td>'
            f'<td><span class="badge badge-{l["type"].lower()}">{l["type"]}</span></td>'
            f'<td class="muted">~{html.escape(str(l["time"]))} min</td></tr>'
            for l in group
        )
        phase_rows.append(
            f'<section><h2>{html.escape(phase_dir.split("-", 1)[0])} · '
            f'{html.escape(phase_dir.split("-", 1)[1].replace("-", " ").title())}</h2>'
            f'<table><thead><tr><th>#</th><th>Lesson</th><th>Type</th><th>Time</th></tr></thead>'
            f"<tbody>{rows}</tbody></table></section>"
        )

    index_html = PAGE_SHELL.format(
        title="Catalog",
        css="style.css",
        sidebar=render_sidebar(lessons, "./index.html"),
        toc="",
        content=(
            '<h1>Discrete Mathematics from Scratch</h1>'
            '<p class="tagline">Prove it. Build it. Verify it with code.</p>'
            + "".join(phase_rows)
        ),
    )
    (SITE_DIR / "index.html").write_text(index_html, encoding="utf-8")

    for lesson in lessons:
        lesson["current"] = True
        page = PAGE_SHELL.format(
            title=html.escape(lesson["title"]),
            css="../style.css",
            sidebar=render_sidebar(lessons, "../index.html"),
            toc=render_toc(lesson["html"]),
            content=(
                f'<p class="crumbs">{html.escape(lesson["phase_num"])} · '
                f'{html.escape(lesson["phase_name"])}</p>'
                f'<span class="badge badge-{lesson["type"].lower()}">{lesson["type"]}</span> '
                f'<span class="muted">~{html.escape(str(lesson["time"]))} min</span>'
                + lesson["html"]
                + lesson["quiz_data"]
                + '<script src="../quiz.js"></script>'
            ),
        )
        lesson["current"] = False
        (SITE_DIR / "lesson" / f"{lesson['slug']}.html").write_text(page, encoding="utf-8")


def main() -> None:
    lessons = discover_lessons()
    if not lessons:
        print("No lessons found under phases/. Nothing to build.")
        return
    build(lessons)
    print(f"Built {len(lessons)} lessons into site/ "
          f"({len(list((SITE_DIR / 'lesson').glob('*.html')))} lesson pages).")


if __name__ == "__main__":
    main()
