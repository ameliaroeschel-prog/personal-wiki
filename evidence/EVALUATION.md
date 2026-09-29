# Evaluation: ask tests, mode checks, failures

**Model:** `mlx-community/gemma-4-e2b-it-4bit` (Gemma 4 E2B instruction-tuned, MLX 4-bit), run locally on an Apple M1 with 8 GB and Wi-Fi off.
**Data:** 5 sources in `vault/raw/`, 18 reviewed notes in `vault/wiki/`, and 129 BM25 passages.
**Final offline run:** [`offline/offline-demo-20260929-150746.log`](offline/offline-demo-20260929-150746.log), screenshot [`screenshots/07-final-offline-run-terminal.webp`](screenshots/07-final-offline-run-terminal.webp).

The questions and expected evidence were written before `ask` was built. They are in [`../tests/questions.md`](../tests/questions.md), outside the vault, so retrieval can never see the answer key.

I evaluated **retrieval** first (did the expected passage come back?), then the **answer** (does each claim follow from a cited passage?). Citations were checked by opening each cited passage. The harness also checks that every `[S#]` refers to a retrieved passage.

## The four ask tests (final offline run, 2026-09-29 15:08)

| # | Question | Expected passage retrieved? | Answer | Citation verified | Result |
|---|---|---|---|---|---|
| 1 | What exploration rate did I use in my final Pac-Man run? | ✅ rank 1: `raw/pacman-dqn-readme.md` › Hyperparameters | "0.09 [S3]" | S3 (reviewed Ms Pac-Man note) states "exploration rate 0.09" ✅ | **Pass** |
| 2 | How much bigger did the word list get when I added the food files? *(paraphrase)* | ⚠️ rank 2: `raw/custom-llm-readme.md` › Corpus details (rank 1 was an unrelated reflections passage) | "grew from 136 to 324 words [S3]" | S3 (Corpus note) states "136 to 324 words" ✅; S2 (raw) also does | **Pass** (retrieval weaker) |
| 3 | Which of my projects ran on Google Colab, and what hardware did each use? *(two sources)* | ✅ both: Pac-Man › Training Statistics & Hardware (rank 1); Custom LLM › Run facts (rank 3) | Pac-Man: NVIDIA T4 GPU [S1][S4]; Custom LLM: Colab CPU [S3] | S1 and S4 contain "T4"; S3 contains "Colab CPU" ✅ | **Pass** |
| 4 | What grade did I receive on the Pac-Man assignment? *(unanswerable)* | n/a: top passages are Pac-Man notes that mention no grade | "INSUFFICIENT EVIDENCE: the wiki does not say what grade was received…" | No citations ✅ | **Pass** |

Evidence cards (question, every retrieved passage with path, section and score, the answer, the citation check and timing):
[Test 1](ask/20260929-150812-what-exploration-rate-did-i-use-in-my-fi.md) ·
[Test 2](ask/20260929-150819-how-much-bigger-did-the-word-list-get-wh.md) ·
[Test 3](ask/20260929-150828-which-of-my-projects-ran-on-google-colab.md) ·
[Test 4](ask/20260929-150904-what-grade-did-i-receive-on-the-pac-man-.md)

Earlier runs are kept for comparison: the online dry run on 2026-09-27 (`ask/20260927-1643*`) and the first offline run on 2026-09-29 (`ask/20260929-1459*`). All four tests passed with the same answers in every run.

**Notes on the answers.**
- **Test 1:** Gemma wrote `$0.09$`, adding LaTeX dollar signs. That's a cosmetic issue, not a factual one.
- **Tests 1 and 2:** the answers cite the reviewed wiki notes rather than the raw README, although the raw passage was also retrieved and supports the same claim. Both are acceptable evidence, since wiki notes carry section references back to raw.
- **Test 3:** the Pac-Man hardware claim is repeated, once for each of the two passages that support it. Redundant, but accurate.
- **Test 2 retrieval:** keyword search did not know that "word list" means "vocabulary". The right passage still reached rank 2, because "food files" matched. This is the limitation discussed in the README.

## Mode-boundary checks (final offline run)

Full transcript: [`chat/20260929-150857-chat-session.md`](chat/20260929-150857-chat-session.md). Each reply is followed by the harness's retrieval decision and the reason for it.

| Check | Input | Expected | Actual | Result |
|---|---|---|---|---|
| Casual | "what can we do?" | Capabilities, no notes search, no refusal | Friendly description, `retrieval: no — conversational` | ✅ |
| Capabilities | "what can you help me with?" | Accurate capability list | Drafting, summarizing, wiki lookup, explaining projects; `retrieval: no` | ✅ |
| Draft | "draft a short 4-step plan for studying for my final exams" | A plan, labeled as a suggestion, no unrelated citations | "Suggestion: …" 4 steps, `retrieval: no — drafting request`, no [S#] | ✅ |
| Follow-up | "make that shorter" | Uses the conversation | Condensed the same 4 steps, `retrieval: no` | ✅ |
| Claim made only in chat | "by the way, I got an A on the Pac-Man assignment" | Chat may respond, but the claim must not become evidence | Scout congratulated her and cited real Pac-Man passages; it did not cite anything for the grade | ✅ |
| Chat retrieves when useful | "when does my conflict lab class meet?" | Looks up notes and cites | "Thursdays from 2 to 5 p.m. in room N500 [S1]" from Haas Course Schedule › Conflict Lab | ✅ |
| Search | `./wiki search "replay memory plateau" -k 3` | Original passages and paths, no generated answer | 3 passages with path, section and BM25 score; model never loaded | ✅ |
| Ask ignores chat | Test 4, run *after* the chat claim above | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | ✅ |

## Failures found and fixed (kept as evidence)

| # | When | What went wrong | Cause | Fix | Re-test |
|---|---|---|---|---|---|
| 1 | First ingest, 09-27 | Gemma linked unrelated concepts ("Learning Rate" on the networking app) and wrote "not explicitly mentioned in the source" | Prompt said "prefer reusing existing concept names" | Prompt: only list concepts the source discusses. Harness: drop concepts whose usage says "not mentioned / implied" | [`ingest/attempt-1`](ingest/attempt-1/NOTES.md), then attempt 2; the rest was fixed in human review |
| 2 | Review, 09-27 | Custom LLM note said "83.3% accuracy on the 48-case suite" (it was **scorable** accuracy; all-case was 41.7%) and misstated the next experiment | Summarization error by the 2B model | Corrected in the wiki note (raw unchanged). `review_notes` records it | [`ingest/attempt-2`](ingest/attempt-2/) vs the current note |
| 3 | Chat test, 09-27 | "what learning rate did I use in my pac-man project?" retrieved "Related projects" link lists; Scout said the value wasn't in the notes | Short link-list sections score high in BM25 | Chunker skips navigation sections and merges sections under 200 chars | [`chat/20260927-164217`](chat/20260927-164217-chat-session.md) → search now ranks the Hyperparameters passage in the top 2 |
| 4 | Ingest, 09-29 | Courses note: Gemma wrote about 1 of 5 courses and titled the page after it | A small model anchors on one topic in a multi-topic source | Rewritten in review as `Haas Course Schedule` | [`ingest/attempt-3-courses`](ingest/attempt-3-courses/NOTES.md) |
| 5 | Ingest, 09-29 | Career note dropped nearly all dates and wrote "Taught for America" | Summary too compressed | Rewritten in review with a dated timeline | [`ingest/attempt-4-career`](ingest/attempt-4-career/NOTES.md) |
| 6 | First offline run, 09-29 14:59 | "draft a study plan for my final exams" pulled in nanoGPT eval passages and built the plan from them | "final" and "exam" crossed the strong-match BM25 threshold after new notes were added | Router: drafting requests never retrieve unless they mention notes or projects | [`chat/20260929-145944`](chat/20260929-145944-chat-session.md) (fail) |
| 7 | Chat re-check, 09-29 15:04 | The plan had **invented citations [S1]–[S4]** with no passages retrieved | Gemma imitates citation format from the persona instructions | Persona: no [S#] without passages. Harness: removes any [S#] that doesn't match a retrieved passage and says so | [`chat/20260929-150446`](chat/20260929-150446-chat-session.md) (fail) → final run [`chat/20260929-150857`](chat/20260929-150857-chat-session.md) (pass) |
