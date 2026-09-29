# Search evidence card

- **Time:** 2026-09-27T16:42:49
- **Model:** `mlx-community/gemma-4-e2b-it-4bit`  ·  **Execution:** local  ·  **Mode:** search

## Question

How much bigger did the word list get when I added the food files?

## Retrieved passages

**** `raw/custom-llm-readme.md` — Building a Custom LLM — Class 4 Assignment > 10. One limitation + proposed next experiment > My questions along the way (reflections) (BM25 10.96)

> - *"The Exp 2 loss graph doesn't look better than Exp 1."* — Correct, and it taught me that **loss measures corpus fit, not exam performance, and isn't comparable across vocabularies.** The real gain is in eval coverage/accuracy.
> - *"Would reasoning emerge with a much bigger vocabulary and millions of training steps?"* — Not from steps alone. **Three things must scale together: far more varied data, a much bigger/deeper model (hundreds of billions of params vs my ~124k), and more compute.** Millions of steps on *this* tiny setup would just **overfit** — memorize the 163 sentences harder — which the flat loss curve past step ~1,200 already hints at. Even frontier models are doing sophisticated next-word prediction at scale, the *same core operation* my model does; scale is what makes reasoning-like behavior emerge.
> 
> ---

**** `raw/custom-llm-readme.md` — Building a Custom LLM — Class 4 Assignment > 2. My three choices, and why > Corpus details (BM25 9.11)

> - **Sources & permissions:** all corpus files are original sentences I wrote for this assignment (`corpus/food_negation.txt`, `corpus/food_opposites.txt`, `corpus/food_sequence.txt`). No copyrighted, confidential, or personal data. Free to share.
> - **Format / extraction check:** all three are UTF-8 **plain text** (`.txt`), so no PDF extraction or OCR was needed. The corpus manifest recorded **0 warnings** for all three files ([corpus_manifest.json](llm_runs/exp2_extended/corpus_manifest.json)).
> - **Passages added:** 163 unique passages (negation 84, opposites 33, sequence 46), split at ≤47 tokens on sentence boundaries.
> - **Vocabulary:** grew from **136 → 324 words**. Unknown-token rates: **training 0.0%**, held-out validation **0.23%** ([vocabulary_report.json](llm_runs/exp2_extended/vocabulary_report.json)).
> - **Split:** duplicates removed, then a 90/10 passage split — Exp 2: **4,279 train / 476 validation** passages. Validation passages never supply weight updates.

**** `wiki/Concepts/Corpus.md` — Corpus (BM25 8.87)

> The collection of text used to train a language model. A small model can only use words that appear in its corpus.
> 
> Appears in: - [[Custom nanoGPT LLM]] — the only variable changed between experiments; three food files grew vocabulary from 136 to 324 words.

**** `raw/custom-llm-readme.md` — Building a Custom LLM — Class 4 Assignment > 6. Loss & samples (part 3) (BM25 8.34)

> | Stage | Exp 2 sample |
> |---|---|
> | **Untrained (step 0)** | `pear professor bond doctor course harvest team physician journey...` — word salad, includes `<UNK>` |
> | **Halfway (step 1,500)** | `our school has a question about the new educator and lesson.` — real grammar appears |
> | **Final (step 3,000)** | `the different mango was mentioned in the harvest report yesterday.` — grammatical, and a food word (`mango`) has bled in |
> 
> **Visible change:** from random word lists → grammatical sentences that echo the corpus. The food vocabulary appears only occasionally in samples because the 163 food passages are just **3.4%** of the corpus — a dilution that matters for §8.
> 
> ---

