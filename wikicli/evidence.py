"""Save every ask/chat/search run so results can be inspected without rerunning the model."""
import json
import re
from datetime import datetime

from . import config


def save(mode, name, record):
    """Write evidence/<mode>/<timestamp>-<slug>.json and a readable .md card. Returns md path."""
    folder = config.EVIDENCE_DIR / mode
    folder.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    slug = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")[:40]
    base = folder / f"{stamp}-{slug}"
    record = {"timestamp": datetime.now().isoformat(timespec="seconds"),
              "model": config.MODEL_ID, "execution": config.EXECUTION_MODE, **record}
    base.with_suffix(".json").write_text(json.dumps(record, indent=2), encoding="utf-8")
    base.with_suffix(".md").write_text(card(mode, record), encoding="utf-8")
    return base.with_suffix(".md")


def card(mode, r):
    lines = [f"# {mode.capitalize()} evidence card", "",
             f"- **Time:** {r['timestamp']}",
             f"- **Model:** `{r['model']}`  ·  **Execution:** {r['execution']}  ·  **Mode:** {mode}"]
    if "stats" in r:
        s = r["stats"]
        lines.append(f"- **Generation:** {s.get('seconds')} s, peak memory {s.get('peak_memory_gb')} GB, "
                     f"{s.get('prompt_tokens')} prompt tokens")
    if "question" in r:
        lines += ["", "## Question", "", r["question"]]
    if "passages" in r:
        lines += ["", "## Retrieved passages", ""]
        for p in r["passages"]:
            lines += [f"**{p.get('label', '')}** `{p['path']}` — {p['section']} (BM25 {p['score']})", "",
                      "> " + p["text"].replace("\n", "\n> "), ""]
    if "answer" in r:
        lines += ["## Answer", "", r["answer"], ""]
    if "citation_check" in r:
        c = r["citation_check"]
        lines += ["## Citation check", "", f"- Cited: {c['cited'] or 'none'}",
                  f"- Invalid (not retrieved): {c['invalid'] or 'none'}", f"- Verdict: {c['verdict']}", ""]
    if "transcript" in r:
        lines += ["## Transcript", ""]
        for t in r["transcript"]:
            tag = f" _(retrieved: {', '.join(t['sources'])})_" if t.get("sources") else " _(no retrieval)_" if t["role"] == "assistant" else ""
            lines += [f"**{t['role']}**{tag}:", "", t["content"], ""]
    return "\n".join(lines) + "\n"
