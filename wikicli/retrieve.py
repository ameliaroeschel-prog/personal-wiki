"""The retrieval tool: BM25 keyword search over local passages. No model, no network.

BM25 scores a passage higher when it contains the query's words, especially words that are
rare across the whole wiki (like "exploration") rather than common ones (like "project").
"""
import json
import math
import re
from collections import Counter

from . import chunker, config

STOPWORDS = set(
    """a an and are as at be been but by can did do does for from had has have how i if in
    into is it its me my of on or our so than that the their them then there these they this
    to was we were what when where which who why will with would you your about did
    """.split()
)


def tokenize(text):
    words = re.findall(r"[a-z0-9]+(?:\.[0-9]+)?", text.lower())
    out = []
    for w in words:
        if w in STOPWORDS or len(w) < 2 and not w.isdigit():
            continue
        # tiny stemmer: "episodes" -> "episode", "learning" -> "learn"
        for suffix in ("ing", "es", "s"):
            if len(w) > 4 and w.endswith(suffix):
                w = w[: -len(suffix)]
                break
        out.append(w)
    return out


def build_index():
    """Chunk every raw source and wiki note, save to data/chunks.json. Returns passage count."""
    passages = []
    for kind, folder in (("raw", config.RAW_DIR), ("wiki", config.WIKI_DIR)):
        for path in sorted(folder.rglob("*.md")):
            rel = path.relative_to(config.VAULT).as_posix()
            passages += chunker.chunk_file(path, rel, kind)
    config.DATA_DIR.mkdir(exist_ok=True)
    config.CHUNKS_FILE.write_text(json.dumps(passages, indent=1), encoding="utf-8")
    return len(passages)


def load_passages():
    if not config.CHUNKS_FILE.exists():
        raise FileNotFoundError(
            "No search index yet. Run:  ./wiki ingest vault/raw   (or ./wiki reindex)"
        )
    return json.loads(config.CHUNKS_FILE.read_text(encoding="utf-8"))


def search(query, k=config.TOP_K, kinds=("raw", "wiki")):
    """Return the top-k passages for `query`, each with a BM25 `score`."""
    passages = [p for p in load_passages() if p["kind"] in kinds]
    docs = [tokenize(p["section"] + " " + p["text"]) for p in passages]
    q = tokenize(query)
    if not q or not docs:
        return []

    n = len(docs)
    avg_len = sum(len(d) for d in docs) / n
    df = Counter(term for d in docs for term in set(d))
    k1, b = 1.5, 0.75

    scored = []
    for p, d in zip(passages, docs):
        tf = Counter(d)
        score = 0.0
        for term in set(q):
            if term not in tf:
                continue
            idf = math.log(1 + (n - df[term] + 0.5) / (df[term] + 0.5))
            score += idf * tf[term] * (k1 + 1) / (tf[term] + k1 * (1 - b + b * len(d) / avg_len))
        if score > 0:
            scored.append({**p, "score": round(score, 2)})
    scored.sort(key=lambda p: p["score"], reverse=True)
    return scored[:k]
