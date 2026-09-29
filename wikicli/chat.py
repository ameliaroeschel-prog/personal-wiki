"""Chat mode = personal assistant. Persona + recent conversation; retrieval only when useful."""
import re

from . import config, evidence, llm, retrieve

# Messages about the assistant itself, small talk, or edits to the previous reply: never retrieve.
NO_RETRIEVAL = re.compile(
    r"^(hi|hey|hello|thanks|thank you|ok|cool)\b|what can (we|you)|help me with|who are you|"
    r"\b(make|keep) (that|it|this)\b|\b(shorter|longer|simpler|rephrase|rewrite|reword|another version)\b",
    re.I,
)
# Messages that are clearly about Amelia's own notes or past work: retrieve.
NEEDS_NOTES = re.compile(
    r"\b(my notes?|wiki|did i|have i|my (project|assignment|class|course|run|results?)|"
    r"according to|pac-?man|dqn|nanogpt|custom llm|networking tracker|card catalog)\b",
    re.I,
)
# Drafting/planning requests are about new writing, not Amelia's notes. Without an explicit
# NEEDS_NOTES cue they never retrieve. (Added after the offline run: "draft a study plan for my
# final exams" hit a strong BM25 match on eval passages and pulled in unrelated citations.)
DRAFTING = re.compile(r"^(please )?(draft|write|brainstorm|plan|outline|help me (write|plan|draft|brainstorm))\b", re.I)
STRONG_MATCH = 8.0  # otherwise retrieve only if BM25 finds a very strong match


def decide_retrieval(message):
    """Return (query or None, reason). Kept as plain rules so the decision is easy to audit."""
    if message.lower().startswith("/notes"):
        return message[6:].strip(), "forced by /notes"
    if NO_RETRIEVAL.search(message):
        return None, "conversational / follow-up"
    if NEEDS_NOTES.search(message):
        return message, "mentions Amelia's notes or projects"
    if DRAFTING.search(message):
        return None, "drafting request with no mention of notes"
    top = retrieve.search(message, k=1)
    if top and top[0]["score"] >= STRONG_MATCH:
        return message, f"strong wiki match (BM25 {top[0]['score']})"
    return None, "no strong wiki match"


def reply(history, message):
    """One chat turn. Returns (answer, passages_used, reason)."""
    persona = (config.PROMPTS_DIR / "persona.md").read_text(encoding="utf-8")
    query, reason = decide_retrieval(message)
    passages = retrieve.search(query, k=3) if query else []
    passages = [p for p in passages if p["score"] >= config.MIN_SCORE]
    for i, p in enumerate(passages, 1):
        p["label"] = f"S{i}"

    user_content = message
    if passages:
        blocks = "\n\n".join(f"[{p['label']}] ({p['path']} — {p['section']})\n{p['text']}" for p in passages)
        user_content = (f"Wiki passages retrieved for this message (cite as [S#] if you use them):\n\n"
                        f"{blocks}\n\nAmelia's message: {message}")
    elif query:
        user_content = f"(A wiki lookup found nothing relevant.)\n\nAmelia's message: {message}"

    recent = history[-config.CHAT_HISTORY_TURNS:]
    messages = [{"role": "system", "content": persona}] + recent + [{"role": "user", "content": user_content}]
    answer, _ = llm.generate(messages, max_tokens=config.CHAT_MAX_TOKENS, temperature=0.6)
    answer, removed = strip_invalid_citations(answer, passages)
    print(f"scout > {answer}")
    if removed:
        print(f"[harness: removed citation(s) {', '.join(removed)} — no matching passage was retrieved this turn]")
    return answer, passages, reason


def strip_invalid_citations(answer, passages):
    """Citation check for chat: Gemma sometimes writes [S1]..[S4] with no passages (seen offline,
    2026-09-29). Any [S#] that doesn't match a passage retrieved THIS turn is removed."""
    valid = {p["label"] for p in passages}
    removed = sorted({c for c in re.findall(r"\[(S\d+)\]", answer) if c not in valid})
    for c in removed:
        answer = re.sub(rf"\s?\[{c}\]", "", answer)
    return answer, removed


def run():
    llm.load()
    history, transcript = [], []
    print(f"\nScout (chat mode) · model {config.MODEL_ID} · execution: {config.EXECUTION_MODE}")
    print("Type a message. /notes <q> forces a wiki lookup, /clear resets, /exit quits.\n")
    while True:
        try:
            msg = input("you > ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if not msg:
            continue
        if msg == "/exit":
            break
        if msg == "/clear":
            history.clear()
            print("[conversation cleared]\n")
            continue

        answer, passages, reason = reply(history, msg)
        sources = [f"{p['label']} {p['path']} — {p['section']}" for p in passages]
        print(f"[retrieval: {'yes' if passages else 'no'} — {reason}]")
        for s in sources:
            print(f"  {s}")
        print()
        # History stores the plain message, not the passages: chat history is conversation, not evidence.
        history += [{"role": "user", "content": msg}, {"role": "assistant", "content": answer}]
        transcript += [{"role": "user", "content": msg},
                       {"role": "assistant", "content": answer, "sources": sources, "reason": reason}]

    if transcript:
        path = evidence.save("chat", "chat-session", {"transcript": transcript})
        print(f"[transcript saved to {path.relative_to(config.ROOT)}]")
