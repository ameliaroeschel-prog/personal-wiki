#!/bin/zsh
# Offline demonstration: run with Wi-Fi OFF. Every command is a fresh CLI process (a "restart").
# Everything printed is also saved to evidence/offline/offline-demo-<timestamp>.log
cd "$(dirname "$0")/.."
mkdir -p evidence/offline
# ./scripts/offline-demo.sh        full demo
# ./scripts/offline-demo.sh chat   offline proof + chat mode checks only (re-check after a fix)
PART="${1:-all}"
LOG="evidence/offline/offline-demo-$( [[ $PART == chat ]] && print chat-recheck- )$(date +%Y%m%d-%H%M%S).log"

step() { print "\n\n==================== $1 ====================\n$ $2"; }

{
  step "0. Proof of offline + device" "curl -sS -m 5 https://huggingface.co"
  date
  if curl -sS -m 5 -o /dev/null https://huggingface.co 2>&1; then
    print "INTERNET IS REACHABLE — turn Wi-Fi off and run this again."; exit 1
  fi
  print "Confirmed: internet unreachable."
  sw_vers | tr '\n' ' '; print
  print "Chip: $(sysctl -n machdep.cpu.brand_string) · RAM: $(( $(sysctl -n hw.memsize) / 1073741824 )) GB unified memory"
  print "Free disk: $(df -h ~ | tail -1 | awk '{print $4}')"
  print "Runtime: $(~/local-ai/venv/bin/python -c 'import mlx_vlm, mlx.core as mx; print("mlx-vlm", mlx_vlm.__version__, "· mlx", mx.__version__)')"

  if [[ $PART != chat ]]; then
  step "1. Help" "./wiki --help"
  ./wiki --help

  step "2a. Ingest all sources (reviewed notes are skipped; index + search index rebuilt)" "./wiki ingest vault/raw"
  ./wiki ingest vault/raw
  step "2b. Ingest a source with local Gemma (draft to data/drafts/, vault untouched)" "./wiki ingest vault/raw/pacman-dqn-readme.md --draft"
  ./wiki ingest vault/raw/pacman-dqn-readme.md --draft
  step "2c. Link check (no duplicates, no broken links)" "./wiki check"
  ./wiki check

  step "3. Ask Test 1 (with memory + time measurement)" "/usr/bin/time -l ./wiki ask \"What exploration rate did I use in my final Pac-Man run?\""
  /usr/bin/time -l ./wiki ask "What exploration rate did I use in my final Pac-Man run?" 2>&1 | grep -vE "^ +[0-9]+ +(involuntary|voluntary|signals|messages|block|page|swaps|average|instructions|cycles)"
  step "4. Ask Test 2 (paraphrased)" "./wiki ask \"How much bigger did the word list get when I added the food files?\""
  ./wiki ask "How much bigger did the word list get when I added the food files?"
  step "5. Ask Test 3 (two sources)" "./wiki ask \"Which of my projects ran on Google Colab, and what hardware did each use?\""
  ./wiki ask "Which of my projects ran on Google Colab, and what hardware did each use?"

  fi

  step "6. Chat mode checks (capabilities, draft, follow-up, a claim made only in chat)" "./wiki chat"
  printf '%s\n' \
    "what can we do?" \
    "what can you help me with?" \
    "draft a short 4-step plan for studying for my final exams" \
    "make that shorter" \
    "by the way, I got an A on the Pac-Man assignment" \
    "when does my conflict lab class meet?" \
    "/exit" | ./wiki chat

  if [[ $PART != chat ]]; then
  step "7. Search mode: original passages only, no model" "./wiki search \"replay memory plateau\" -k 3"
  ./wiki search "replay memory plateau" -k 3

  step "8. Ask Test 4 (unanswerable) — also checks the chat claim above is NOT treated as evidence" "./wiki ask \"What grade did I receive on the Pac-Man assignment?\""
  ./wiki ask "What grade did I receive on the Pac-Man assignment?"

  fi

  step "Done" "date"
  date
} 2>&1 | tee "$LOG"
print "\nSaved full log to $LOG"
