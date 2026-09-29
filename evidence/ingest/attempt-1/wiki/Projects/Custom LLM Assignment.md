---
type: source-note
source_id: custom-llm-readme
source_path: raw/custom-llm-readme.md
source_sha256: c647621eff21139e
description: "This document details two experiments training a tiny language model from scratch using the nanoGPT framework, focusing on how corpus change"
generated_by: mlx-community/gemma-4-e2b-it-4bit
ingested: 2026-09-27
reviewed: false
---

# Custom LLM Assignment

This document details two experiments training a tiny language model from scratch using the nanoGPT framework, focusing on how corpus changes affect performance. The main result shows that expanding the corpus improves model performance, although the model struggles with reasoning tasks.

## Key details

- The model uses a word-token variant with 2 blocks, 4 heads, 64-dim embeddings, and a 48-token context.
- Experiment 1 used the starter "classroom" sentences only, while Experiment 2 included 3 food/restaurant files.
- Training steps were set to 3,000 for both experiments, and the learning rate was 0.001.
- Experiment 2 resulted in more parameters (123,904 vs 111,872 for Exp 1) due to a larger vocabulary.
- The model learns to predict the next word by nudging its weights to be less wrong based on the corpus patterns.
- The model shows a limitation in reasoning, as it learns vocabulary and surface grammar but not complex reasoning.
- A proposed next experiment is to hold the corpus fixed and scale the training.

## Related concepts

- [[Learning Rate]] — The learning rate was set to 0.001 for both experiments.
- [[Corpus]] — The corpus was varied between the baseline classroom sentences and the extended set including food/restaurant files.
- [[Loss]] — Loss values were tracked across training steps to observe model convergence.
- [[Evaluation Suite]] — The evaluation suite is used as the study material to test the model's learned patterns.

## Sources

- Original: [[raw/custom-llm-readme.md]] (unchanged copy in `vault/raw/`)
