"""Ask mode = the RAG workflow: retrieve -> build evidence prompt -> Gemma -> check citations.

Each question is standalone: no chat history and no persona are ever included.
"""
import re

from . import config, evidence, llm, retrieve

INSUFFICIENT = "INSUFFICIENT EVIDENCE"


def build_messages(question, passages):
    rules = (config.PROMPTS_DIR / "wiki-instructions.md").read_text(encoding="utf-8")
    blocks = [f"[{p['label']}] ({p['path']} — {p['section']})\n{p['text']}" for p in passages]
    user = "Source passages:\n\n" + "\n\n".join(blocks) + f"\n\nQuestion: {question}"
    return [{"role": "system", "content": rules}, {"role": "user", "content": user}]


def check_citations(answer, passages):
    labels = {p["label"] for p in passages}
    cited = sorted(set(re.findall(r"\[(S\d+)\]", answer)))
    invalid = [c for c in cited if c not in labels]
    if answer.upper().startswith(INSUFFICIENT):
        verdict = "insufficient evidence reported" + (" (but cites sources!)" if cited else "")
    elif not cited:
        verdict = "FAIL: answer has no citations"
    elif invalid:
        verdict = "FAIL: cites passages that were not retrieved"
    else:
        verdict = "ok: all citations point to retrieved passages (still verify they support the claims)"
    return {"cited": cited, "invalid": invalid, "verdict": verdict}


def run(question, save=True):
    passages = retrieve.search(question, k=config.TOP_K)
    for i, p in enumerate(passages, 1):
        p["label"] = f"S{i}"

    if not passages or passages[0]["score"] < config.MIN_SCORE:
        # Nothing relevant enough to show the model: refuse without calling Gemma.
        answer, stats = f"{INSUFFICIENT}: no wiki passage matched this question.", {"seconds": 0}
    else:
        answer, stats = llm.generate(build_messages(question, passages),
                                     max_tokens=config.ASK_MAX_TOKENS, temperature=0.1)
    check = check_citations(answer, passages)
    record = {"question": question, "passages": passages, "answer": answer,
              "citation_check": check, "stats": stats}
    path = evidence.save("ask", question, record) if save else None
    return record, path
