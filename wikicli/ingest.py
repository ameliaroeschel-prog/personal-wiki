"""Ingestion: raw source -> local Gemma -> wiki note + concept notes -> index.md + search index.

Duplicate-safe by design:
- data/source_catalog.json pins each source (by filename) to ONE note path on first ingest,
  so re-ingesting overwrites that note instead of creating a new one.
- Notes whose frontmatter says `reviewed: true` are never overwritten unless --force.
"""
import hashlib
import json
import re
from datetime import date

from . import chunker, config, llm, retrieve

FOLDERS = {"Projects", "Courses", "Career"}
# Gemma sometimes lists a concept and then admits the source doesn't discuss it; drop those links.
NOT_IN_SOURCE = re.compile(r"not (explicitly )?(mentioned|discussed|covered)|\bimplied\b|does not (mention|discuss)", re.I)


# ---------- small helpers ----------

def load_catalog():
    if config.CATALOG_FILE.exists():
        return json.loads(config.CATALOG_FILE.read_text(encoding="utf-8"))
    return {}


def save_catalog(catalog):
    config.DATA_DIR.mkdir(exist_ok=True)
    config.CATALOG_FILE.write_text(json.dumps(catalog, indent=2), encoding="utf-8")


def clean_title(raw, fallback):
    """Readable filename: letters/digits/spaces/hyphens, max 6 words, Title Case."""
    t = re.sub(r"[^A-Za-z0-9 \-]", " ", raw or "").strip()
    words = t.split()[:6]
    if not words:
        return fallback
    return " ".join(w if w.isupper() or any(c.isdigit() for c in w) else w[0].upper() + w[1:] for w in words)


def read_frontmatter(path):
    if not path.exists():
        return {}
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return {}
    block = text[3 : text.find("\n---", 3)]
    meta = {}
    for line in block.splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            meta[k.strip()] = v.strip().strip('"')
    return meta


def all_notes():
    """{title: path} for every note in the wiki."""
    return {p.stem: p for p in config.WIKI_DIR.rglob("*.md")}


def digest(text, limit=config.INGEST_INPUT_CHARS):
    """Fit a long source into Gemma's budget: every heading plus the start of its section."""
    secs = list(chunker.sections(text))
    if len(text) <= limit or not secs:
        return text[:limit]
    per = max(200, limit // len(secs))
    return "\n\n".join(f"## {h}\n{body[:per]}" for h, body in secs)[:limit]


def parse_reply(reply):
    """Parse Gemma's TITLE/FOLDER/SUMMARY/DETAILS/CONCEPTS format (tolerant of small slips)."""
    out = {"title": "", "folder": "Projects", "summary": "", "details": [], "concepts": []}
    section = None
    for line in reply.splitlines():
        s = line.strip().strip("*")
        key = s.split(":", 1)[0].strip().upper() if ":" in s else ""
        if key in ("TITLE", "FOLDER", "SUMMARY"):
            val = s.split(":", 1)[1].strip().strip('"*')
            if key == "FOLDER":
                val = val.title() if val.title() in FOLDERS else "Projects"
            out[key.lower()] = val
            section = key
        elif key in ("DETAILS", "CONCEPTS"):
            section = key
        elif s.startswith(("-", "*", "•")) and section == "DETAILS":
            out["details"].append(s.lstrip("-*• ").strip())
        elif s.startswith(("-", "*", "•")) and section == "CONCEPTS":
            parts = [x.strip() for x in s.lstrip("-*• ").split("|")]
            if len(parts) >= 2 and parts[0] and not NOT_IN_SOURCE.search(" ".join(parts[1:])):
                out["concepts"].append({"name": parts[0], "definition": parts[1],
                                        "usage": parts[2] if len(parts) > 2 else ""})
        elif section == "SUMMARY" and s:
            out["summary"] += " " + s
    return out


# ---------- writing notes ----------

def write_source_note(path, title, parsed, source_id, raw_rel, sha):
    concepts = [clean_title(c["name"], "") for c in parsed["concepts"]]
    related = "\n".join(
        f"- [[{name}]] — {c['usage'] or c['definition']}" for name, c in zip(concepts, parsed["concepts"]) if name
    )
    details = "\n".join(f"- {d}" for d in parsed["details"])
    summary = parsed["summary"].strip()
    description = summary.split(". ")[0].rstrip(".")[:140].replace('"', "'")
    path.write_text(
        f"""---
type: source-note
source_id: {source_id}
source_path: {raw_rel}
source_sha256: {sha}
description: "{description}"
generated_by: {config.MODEL_ID}
ingested: {date.today().isoformat()}
reviewed: false
---

# {title}

{summary}

## Key details

{details}

## Related concepts

{related}

## Sources

- Original: [[{raw_rel}]] (unchanged copy in `vault/raw/`)
""",
        encoding="utf-8",
    )


def update_concept_note(name, concept, source_title):
    """Create or update Concepts/<name>.md. The 'Appears in' list gets one line per source note."""
    path = config.WIKI_DIR / "Concepts" / f"{name}.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    entry = f"- [[{source_title}]] — {concept['usage'] or concept['definition']}"
    if path.exists():
        text = path.read_text(encoding="utf-8")
        lines = [l for l in text.splitlines() if not l.startswith(f"- [[{source_title}]]")]
        head, _, tail = "\n".join(lines).partition("## Appears in")
        entries = [l for l in tail.splitlines() if l.startswith("- [[")] + [entry]
        path.write_text(head + "## Appears in\n\n" + "\n".join(sorted(entries)) + "\n", encoding="utf-8")
    else:
        definition = concept["definition"].replace('"', "'")
        path.write_text(
            f"""---
type: concept
description: "{definition[:140]}"
reviewed: false
---

# {name}

{concept['definition']}

## Appears in

{entry}
""",
            encoding="utf-8",
        )


def write_index():
    """vault/index.md: human landing page grouped by folder, one line per note."""
    groups = {}
    for title, path in sorted(all_notes().items()):
        folder = path.parent.name
        desc = read_frontmatter(path).get("description", "")
        groups.setdefault(folder, []).append(f"- [[{title}]] — {desc}")
    order = ["Projects", "Courses", "Career", "Concepts"]
    parts = ["# Index", "",
             "Amelia's personal learning & career wiki. Start here, pick a topic, then follow "
             "each note's **Sources** link back to the original in `raw/`.", ""]
    for folder in sorted(groups, key=lambda f: order.index(f) if f in order else 99):
        parts += [f"## {folder}", ""] + groups[folder] + [""]
    parts += ["## Original sources", ""] + [
        f"- [[raw/{p.name}]]" for p in sorted(config.RAW_DIR.glob("*.md"))
    ] + [""]
    config.INDEX_FILE.write_text("\n".join(parts), encoding="utf-8")


def check_links():
    """Return a list of problems: [[links]] that don't resolve, notes whose heading != filename."""
    targets = set(all_notes()) | {f"raw/{p.name}" for p in config.RAW_DIR.iterdir()}
    problems = []
    for title, path in sorted(all_notes().items()):
        text = path.read_text(encoding="utf-8")
        if f"\n# {title}\n" not in text:
            problems.append(f"{path.relative_to(config.VAULT)}: first heading does not match filename")
        for link in re.findall(r"\[\[([^\]|#]+)", text):
            if link not in targets:
                problems.append(f"{path.relative_to(config.VAULT)}: broken link [[{link}]]")
    for link in re.findall(r"\[\[([^\]|#]+)", config.INDEX_FILE.read_text(encoding="utf-8")):
        if link not in targets:
            problems.append(f"index.md: broken link [[{link}]]")
    return problems


# ---------- main entry ----------

def run(target, force=False, draft=False):
    """Ingest a folder of sources or one source file.

    draft=True: Gemma still reads each source and writes a note, but to data/drafts/ (outside the
    vault), so reviewed notes are never touched. Used to compare a fresh draft with the reviewed note.
    """
    target = target.resolve()
    if target.is_file():
        sources = [target]
    elif target.is_dir():
        sources = sorted(target.glob("*.md")) + sorted(target.glob("*.txt"))
    else:
        raise FileNotFoundError(f"Source not found: {target}")
    if not sources:
        raise FileNotFoundError(f"No .md or .txt files in {target}")

    catalog = load_catalog()
    instructions = (config.PROMPTS_DIR / "ingest-instructions.md").read_text(encoding="utf-8")
    report = []

    for src in sources:
        source_id = src.stem
        raw_rel = src.relative_to(config.VAULT).as_posix() if src.is_relative_to(config.VAULT) else src.name
        text = src.read_text(encoding="utf-8")
        sha = hashlib.sha256(text.encode()).hexdigest()[:16]
        entry = catalog.get(source_id)

        if entry and not draft:
            note_path = config.VAULT / entry["note_path"]
            meta = read_frontmatter(note_path)
            if meta.get("reviewed") == "true" and not force:
                status = "unchanged" if entry["sha256"] == sha else "SOURCE CHANGED (use --force to regenerate)"
                report.append(f"skip   {src.name} -> {entry['note_path']} (reviewed, {status})")
                continue

        existing_concepts = sorted(p.stem for p in (config.WIKI_DIR / "Concepts").glob("*.md"))
        messages = [
            {"role": "system", "content": instructions},
            {"role": "user", "content": f"Existing concept list: {', '.join(existing_concepts) or '(none yet)'}\n\n"
                                        f"Source file: {src.name}\n\n{digest(text)}"},
        ]
        print(f"[ingest] {src.name}: sending {len(messages[1]['content'])} chars to Gemma...", flush=True)
        reply, stats = llm.generate(messages, max_tokens=config.INGEST_MAX_TOKENS, temperature=0.2)
        parsed = parse_reply(reply)

        if draft:
            drafts = config.DATA_DIR / "drafts"
            drafts.mkdir(parents=True, exist_ok=True)
            draft_path = drafts / f"{source_id}.md"
            title = clean_title(parsed["title"], source_id)
            write_source_note(draft_path, title, parsed, source_id, raw_rel, sha)
            report.append(f"draft  {src.name} -> {draft_path.relative_to(config.ROOT)} "
                          f"(Gemma title: '{title}'; {stats['seconds']} s, peak {stats['peak_memory_gb']} GB; vault untouched)")
            continue

        if entry:  # title and folder are pinned: re-ingest updates the same file
            title, note_rel = entry["title"], entry["note_path"]
        else:
            title = clean_title(parsed["title"], clean_title(source_id.replace("-", " "), source_id))
            if title in all_notes():  # meaningful qualifier instead of a random suffix
                title = f"{title} - {parsed['folder']}"
            note_rel = f"wiki/{parsed['folder']}/{title}.md"
        note_path = config.VAULT / note_rel
        note_path.parent.mkdir(parents=True, exist_ok=True)

        write_source_note(note_path, title, parsed, source_id, raw_rel, sha)
        for c in parsed["concepts"]:
            name = clean_title(c["name"], "")
            if name and name != title:
                update_concept_note(name, c, title)

        catalog[source_id] = {"title": title, "note_path": note_rel, "raw_path": raw_rel,
                              "original_filename": src.name, "sha256": sha,
                              "ingested": date.today().isoformat()}
        verb = "update" if entry else "create"
        report.append(f"{verb} {src.name} -> {note_rel}  ({stats['seconds']} s, peak {stats['peak_memory_gb']} GB)")

    if draft:
        return report
    save_catalog(catalog)
    write_index()
    n = retrieve.build_index()
    report.append(f"index.md rewritten; search index rebuilt ({n} passages)")
    return report
