"""Split Markdown into passages that keep their source path and section heading."""
import re

from . import config

HEADING = re.compile(r"^(#{1,6})\s+(.*)")


def strip_frontmatter(text):
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            return text[end + 4 :].lstrip("\n")
    return text


def sections(text):
    """Yield (heading_path, body) for each heading section, e.g. 'Evaluation > Score Comparison'."""
    stack, body, current = [], [], "(top)"
    for line in strip_frontmatter(text).splitlines():
        m = HEADING.match(line)
        if m:
            if "".join(body).strip():
                yield current, "\n".join(body).strip()
            level, title = len(m.group(1)), m.group(2).strip()
            stack = stack[: level - 1] + [title]
            current = " > ".join(stack)
            body = []
        else:
            body.append(line)
    if "".join(body).strip():
        yield current, "\n".join(body).strip()


def split_long(body, limit):
    """Break a long section on blank lines so no passage is much bigger than `limit`."""
    parts, buf = [], ""
    for para in re.split(r"\n\s*\n", body):
        if buf and len(buf) + len(para) > limit:
            parts.append(buf.strip())
            buf = ""
        buf += para + "\n\n"
    if buf.strip():
        parts.append(buf.strip())
    return parts


# Link lists in wiki notes are navigation, not evidence. Indexing them let short link lines
# outrank the real passage (see README, "Retrieval fix"), so they are skipped.
NAV_SECTIONS = ("Related concepts", "Related projects", "Related notes", "Sources")
MIN_SECTION_CHARS = 200  # shorter sections are merged into the previous one


def merged_sections(text, kind):
    merged = []
    for section, body in sections(text):
        if kind == "wiki" and section.split(" > ")[-1] in NAV_SECTIONS:
            continue
        if merged and len(body) < MIN_SECTION_CHARS:
            prev_section, prev_body = merged[-1]
            merged[-1] = (prev_section, prev_body + f"\n\n{section.split(' > ')[-1]}: {body}")
        else:
            merged.append((section, body))
    return merged


def chunk_file(path, rel_path, kind):
    """Return passage dicts for one file. kind is 'raw' (original evidence) or 'wiki' (note)."""
    text = path.read_text(encoding="utf-8")
    passages = []
    for section, body in merged_sections(text, kind):
        for i, piece in enumerate(split_long(body, config.PASSAGE_CHARS)):
            passages.append(
                {
                    "id": f"{rel_path}#{len(passages)}",
                    "path": rel_path,
                    "section": section + (f" (part {i + 1})" if i else ""),
                    "kind": kind,
                    "text": piece,
                }
            )
    return passages
