---
type: source-note
source_id: custom-llm-readme
source_path: raw/custom-llm-readme.md
source_sha256: c647621eff21139e
description: "Assignment 3: a tiny nanoGPT trained from scratch in two corpus experiments; more vocabulary, but no new reasoning"
generated_by: mlx-community/gemma-4-e2b-it-4bit
ingested: 2026-09-27
reviewed: true
review_notes: "Renamed from 'Custom LLM Assignment' and moved Courses/ -> Projects/. Corrected two Gemma errors: 83.3% is scorable accuracy (all-case was 41.7%), and the next experiment scales model depth, not 'the training'."
---

# Custom nanoGPT LLM

Assignment 3: two small experiments training a tiny word-level nanoGPT from scratch, changing only the corpus. Training clearly worked, and adding three food/restaurant files raised eval coverage, but the targeted reasoning categories stayed at zero — **vocabulary ≠ reasoning**.

## Key details

- Model: 2 blocks, 4 heads, 64-dim embeddings, 48-token context; trained on CPU with AdamW (top of source).
- Both experiments: 3,000 training steps, learning rate 0.001 (§ 2. My three choices).
- Experiment 1 used the starter classroom sentences; Experiment 2 added three food files — 163 passages — growing vocabulary **136 → 324 words** (§ Corpus details).
- Exp 1 trained: all-case success 20/48 (41.7%), scorable accuracy 83.3%, coverage 50% (§ 7. Evaluations).
- Exp 2: all-case success 50%, coverage 58%; the gain came mostly from new_wording (4/8 → 8/8), while negation, opposites and sequence stayed at 0 (§ 3, § 8).
- Exp 2 has more parameters (123,904 vs 111,872) only because of the larger vocabulary (§ 4. Run facts).
- Eval prompts and answers were kept out of the training corpus (§ Leakage / separation checks).
- **Next experiment:** hold the corpus fixed and scale model depth (2 → 4 blocks) and/or 10× the targeted teaching data (§ 10).

## Related concepts

- [[Large Language Model]] — this project trains a tiny one from scratch.
- [[Corpus]] — the one variable changed between the two experiments.
- [[Evaluation Suite]] — the fixed 48-case exam, kept separate from the corpus.
- [[Learning Rate]] — held at 0.001; the README explains why too large or too small fails.
- [[Loss]] — plateaued around step 1,200; not comparable across different vocabularies.

## Related projects

- [[Ms Pac-Man DQN Agent]] — the other training experiment; both tune a learning rate and read loss curves.

## Sources

- Original: [[raw/custom-llm-readme.md]] (unchanged copy in `vault/raw/`)
