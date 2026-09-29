"""Command-line entry point. Picks the mode; each mode lives in its own module."""
import argparse
import sys
from pathlib import Path

from . import config

HELP = f"""\
Personal wiki CLI — local Gemma + BM25 retrieval over an Obsidian vault.

Commands:
  ./wiki ingest vault/raw [--force]   Read sources, have local Gemma write linked wiki notes,
                                      update vault/index.md and rebuild the search index.
                                      Reviewed notes (reviewed: true) are skipped unless --force.
                                      Also accepts a single file.
  ./wiki ingest <file> --draft        Gemma writes a fresh draft to data/drafts/ (vault untouched).
  ./wiki search "query" [-k 5]        Show matching ORIGINAL passages + paths. No model, no answer.
  ./wiki ask "question" [--mode local]
                                      Standalone factual answer from retrieved evidence, with
                                      [S#] citations, or INSUFFICIENT EVIDENCE. No chat history.
  ./wiki chat                         Personal assistant "Scout": conversation memory, retrieves
                                      notes only when useful. /notes /clear /exit inside chat.
  ./wiki reindex                      Rebuild index.md + search index without calling the model.
  ./wiki check                        Verify every [[link]] resolves and headings match filenames.
  ./wiki help                         This message.

Configuration (wikicli/config.py):
  model      {config.MODEL_ID}   (execution: local, offline)
  vault      {config.VAULT.relative_to(config.ROOT)}/  (raw/ originals, wiki/ notes, index.md)
  prompts    prompts/persona.md (chat), prompts/wiki-instructions.md (ask),
             prompts/ingest-instructions.md (ingest)
  evidence   every ask/chat/search run is saved to evidence/<mode>/

Requires: ~/local-ai/venv with mlx-vlm, and the model in the local Hugging Face cache.
"""


def print_passages(passages):
    if not passages:
        print("No matching passages.")
    for i, p in enumerate(passages, 1):
        print(f"\n[{i}] {p['path']}  ·  {p['section']}  ·  BM25 {p['score']}  ·  {p['kind']}")
        print("    " + p["text"].replace("\n", "\n    "))


def main(argv=None):
    parser = argparse.ArgumentParser(prog="wiki", add_help=False)
    parser.add_argument("-h", "--help", action="store_true")
    sub = parser.add_subparsers(dest="command")
    p_ing = sub.add_parser("ingest", add_help=False)
    p_ing.add_argument("folder", nargs="?", default=str(config.RAW_DIR))
    p_ing.add_argument("--force", action="store_true")
    p_ing.add_argument("--draft", action="store_true")
    p_s = sub.add_parser("search", add_help=False)
    p_s.add_argument("query", nargs="+")
    p_s.add_argument("-k", type=int, default=5)
    p_s.add_argument("--raw-only", action="store_true")
    p_a = sub.add_parser("ask", add_help=False)
    p_a.add_argument("question", nargs="+")
    p_a.add_argument("--mode", default="local", choices=["local"])
    sub.add_parser("chat", add_help=False)
    sub.add_parser("reindex", add_help=False)
    sub.add_parser("check", add_help=False)
    sub.add_parser("help", add_help=False)

    args = parser.parse_args(argv)
    if args.help or args.command in (None, "help"):
        print(HELP)
        return

    from . import llm  # imported lazily so `search` and `help` never load the model

    try:
        if args.command == "ingest":
            from . import ingest
            for line in ingest.run(Path(args.folder), force=args.force, draft=args.draft):
                print(line)

        elif args.command == "reindex":
            from . import ingest, retrieve
            ingest.write_index()
            print(f"index.md rewritten; search index rebuilt: {retrieve.build_index()} passages")

        elif args.command == "check":
            from . import ingest
            problems = ingest.check_links()
            n = len(ingest.all_notes())
            print("\n".join(problems) if problems else f"All links resolve; all {n} note headings match filenames.")

        elif args.command == "search":
            from . import evidence, retrieve
            query = " ".join(args.query)
            kinds = ("raw",) if args.raw_only else ("raw", "wiki")
            passages = retrieve.search(query, k=args.k, kinds=kinds)
            print(f'search "{query}"  ·  mode: search (no model called)')
            print_passages(passages)
            evidence.save("search", query, {"question": query, "passages": passages})

        elif args.command == "ask":
            from . import ask
            question = " ".join(args.question)
            print(f"ask · model {config.MODEL_ID} · execution: {args.mode} · no chat history")
            record, path = ask.run(question)
            print("\nRetrieved passages:")
            for p in record["passages"]:
                print(f"  [{p['label']}] {p['path']} — {p['section']} (BM25 {p['score']})")
            print(f"\nAnswer:\n{record['answer']}\n")
            print(f"Citation check: {record['citation_check']['verdict']}")
            print(f"Time: {record['stats'].get('seconds')} s · peak memory {record['stats'].get('peak_memory_gb')} GB")
            print(f"Evidence card: {path.relative_to(config.ROOT)}")

        elif args.command == "chat":
            from . import chat
            chat.run()

    except llm.ModelUnavailable as e:
        sys.exit(f"Local model unavailable: {e}")
    except FileNotFoundError as e:
        sys.exit(f"Error: {e}")


if __name__ == "__main__":
    main()
