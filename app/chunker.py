"""Single responsibility: stage 1 of ingestion. Turn the raw MDX docs into data/chunks.jsonl.

Each line is one chunk: {"id", "document", "metadata"}.
- id: stable, built from file path + heading path (never from position), so eval cases survive doc edits.
- metadata.hash: sha256 of the chunk text, so the indexing stage can skip unchanged chunks.
Output is deterministic, so `git diff` on chunks.jsonl shows exactly which chunks a rule change touched.

Run from the project root:  python3 -m app.chunker
"""

import hashlib
import json
import re
import statistics
from pathlib import Path

from app import config

CALLOUTS = {"Note", "Tip", "Warning", "Info", "Check"}
CONTAINERS = {"Tab", "Accordion", "Step", "Card"}

# Inline code is matched first so it is never altered; otherwise match one JSX tag.
_JSX = re.compile(
    r"(?P<code>`[^`\n]*`)"
    r"|<(?P<close>/)?(?P<name>[A-Z][A-Za-z0-9]*)(?P<attrs>(?:\s[^<>]*?)?)\s*/?>"
)
_LINK = re.compile(r"\]\((/[^)\s]+)\)")


def est_tokens(text: str) -> int:
    """Rough token estimate (chars / 4)."""
    return len(text) // 4


def _is_fence(line: str) -> bool:
    return line.lstrip().startswith("```")


def _map_outside_code(text: str, fn) -> str:
    """Apply fn to prose segments only; fenced code blocks pass through untouched."""
    out, buf, in_code = [], [], False
    for line in text.split("\n"):
        if _is_fence(line):
            if not in_code and buf:
                out.append(fn("\n".join(buf)))
                buf = []
            in_code = not in_code
            out.append(line)
        elif in_code:
            out.append(line)
        else:
            buf.append(line)
    if buf:
        out.append(fn("\n".join(buf)))
    return "\n".join(out)


def _jsx(m: re.Match) -> str:
    if m.group("code"):
        return m.group("code")
    if m.group("close"):
        return ""
    name = m.group("name")
    if name in CALLOUTS:
        return f"**{name}:** "
    if name in CONTAINERS:
        t = re.search(r'title="([^"]*)"', m.group("attrs") or "")
        return f"**{t.group(1)}**\n" if t else ""
    return ""


def _fix_link(m: re.Match) -> str:
    path = m.group(1)
    if path.startswith("/oss/") and not path.startswith(("/oss/python/", "/oss/javascript/")):
        path = "/oss/python/" + path[len("/oss/"):]
    return f"]({config.DOCS_SITE}{path})"


def _clean_prose(seg: str) -> str:
    seg = re.sub(r"\{/\*.*?\*/\}", "", seg, flags=re.S)       # MDX comments
    seg = re.sub(r"^<a id=[^>]*/>\n?", "", seg, flags=re.M)    # anchor stubs
    seg = re.sub(r"^import .+ from .+\n?", "", seg, flags=re.M)  # MDX imports
    seg = _JSX.sub(_jsx, seg)
    return _LINK.sub(_fix_link, seg)


def clean(raw: str) -> tuple[dict, str]:
    """Return (frontmatter dict, cleaned Python-only body text)."""
    text = raw.replace("\r\n", "\n")
    meta = {}
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if m:
        for line in m.group(1).splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                meta[k.strip()] = v.strip().strip("\"'")
        text = text[m.end():]
    # Markers can be indented (inside <Tab> etc.), so allow leading whitespace.
    text = re.sub(r"^[ \t]*:::js[ \t]*\n.*?^[ \t]*:::[ \t]*\n?", "", text, flags=re.S | re.M)  # drop JS blocks
    text = re.sub(r"^[ \t]*:::python[ \t]*\n(.*?)^[ \t]*:::[ \t]*\n?", r"\1", text, flags=re.S | re.M)  # keep Python
    text = _map_outside_code(text, _clean_prose)
    text = re.sub(r"[ \t]*(?:#|//) \[!code[^\]]*\]", "", text)  # docs-site highlight hints inside code
    return meta, re.sub(r"\n{3,}", "\n\n", text).strip()


def sections(text: str) -> list[tuple[list[str], str]]:
    """Split on ##/### headings (ignoring '#' inside code). Returns [(heading_path, body)]."""
    out, stack, buf, in_code = [], [], [], False

    def flush():
        body = "\n".join(buf).strip()
        if body:
            out.append(([t for _, t in stack], body))
        buf.clear()

    for line in text.split("\n"):
        if _is_fence(line):
            in_code = not in_code
        h = None if in_code else re.match(r"^(#{2,3}) (.+)", line)
        if h:
            flush()
            level = len(h.group(1))
            stack[:] = [(lv, t) for lv, t in stack if lv < level]
            stack.append((level, h.group(2).strip()))
        else:
            buf.append(line)
    flush()
    return out


def split_big(body: str) -> list[str]:
    """Split an oversize section on blank lines, never inside a code fence (or a table)."""
    blocks, cur, in_code = [], [], False
    for line in body.split("\n"):
        if _is_fence(line):
            in_code = not in_code
        if line.strip() == "" and not in_code and cur:
            blocks.append("\n".join(cur))
            cur = []
        else:
            cur.append(line)
    if cur:
        blocks.append("\n".join(cur))
    parts, acc = [], ""
    for b in blocks:
        if acc and est_tokens(acc + b) > config.MAX_CHUNK_TOKENS:
            parts.append(acc.strip())
            acc = ""
        acc += b + "\n\n"
    if acc.strip():
        parts.append(acc.strip())
    return parts


def slug(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def chunk_file(path: Path, docs_dir: Path) -> list[dict]:
    rel = path.relative_to(docs_dir)
    rel_noext = rel.with_suffix("").as_posix()
    meta, body = clean(path.read_text(encoding="utf-8"))
    title = meta.get("title", path.stem)
    chunks, used = [], set()
    for heading_path, text in sections(body):
        base = f"{rel_noext}#{'/'.join(slug(h) for h in heading_path) or 'intro'}"
        n = 2
        while base in used:  # same heading used twice in one file
            base, n = f"{base.split('~')[0]}~{n}", n + 1
        used.add(base)
        parts = split_big(text) if est_tokens(text) > config.MAX_CHUNK_TOKENS else [text]
        header = " > ".join([title] + heading_path)
        if not heading_path and meta.get("description"):
            header += f"\n{meta['description']}"
        for i, part in enumerate(parts, 1):
            doc = f"{header}\n\n{part}"
            chunks.append({
                "id": base if len(parts) == 1 else f"{base}-{i}",
                "document": doc,
                "metadata": {
                    "source": rel.as_posix(),
                    "title": title,
                    "section": " > ".join(heading_path) or "(intro)",
                    "url": f"{config.DOCS_SITE}{config.DOCS_URL_PREFIX}/{rel_noext}",
                    "lang": "python",
                    "has_code": "```" in part,
                    "tokens": est_tokens(doc),
                    "hash": hashlib.sha256(doc.encode("utf-8")).hexdigest()[:16],
                },
            })
    return chunks


def build_chunks(docs_dir: Path = config.DOCS_DIR) -> list[dict]:
    """Chunk every .md/.mdx file under docs_dir, in sorted path order."""
    files = sorted(p for p in docs_dir.rglob("*") if p.suffix in {".md", ".mdx"})
    chunks = [c for f in files for c in chunk_file(f, docs_dir)]
    ids = [c["id"] for c in chunks]
    dupes = {i for i in ids if ids.count(i) > 1}
    if dupes:
        raise ValueError(f"duplicate chunk ids: {sorted(dupes)}")
    return chunks


def write_jsonl(chunks: list[dict], path: Path = config.CHUNKS_PATH) -> None:
    lines = (json.dumps(c, ensure_ascii=False) for c in chunks)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    chunks = build_chunks()
    write_jsonl(chunks)
    toks = [c["metadata"]["tokens"] for c in chunks]
    files = {c["metadata"]["source"] for c in chunks}
    print(f"wrote {len(chunks)} chunks from {len(files)} files -> {config.CHUNKS_PATH}")
    print(f"tokens min/median/max: {min(toks)}/{int(statistics.median(toks))}/{max(toks)}")
    print(f"over MAX_CHUNK_TOKENS ({config.MAX_CHUNK_TOKENS}): {sum(t > config.MAX_CHUNK_TOKENS for t in toks)}")
    print(f"over 256 (would be truncated by MiniLM): {sum(t > 256 for t in toks)}")
    print(f"chunks with leftover ':::' markers: {sum(':::' in c['document'] for c in chunks)}")


if __name__ == "__main__":
    main()
