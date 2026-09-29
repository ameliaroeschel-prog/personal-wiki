---
type: source-note
source_id: custom-llm-readme
source_path: raw/custom-llm-readme.md
source_sha256: c647621eff21139e
description: "This document details the process of training a tiny language model from scratch using the nanoGPT framework and analyzing its performance a"
generated_by: mlx-community/gemma-4-e2b-it-4bit
ingested: 2026-09-27
reviewed: false
---

# Custom LLM Assignment

This document details the process of training a tiny language model from scratch using the nanoGPT framework and analyzing its performance across different corpus variations. The main result is observing how training steps and corpus size affect model performance and evaluation accuracy.

## Key details

- The model uses a word-token variant with 2 blocks, 4 heads, 64-dim embeddings, and a 48-token context.
- Experiment 1 used the starter "classroom" sentences only, while Experiment 2 included 3 food/restaurant files.
- Training steps were set to 3,000 for both experiments, and the learning rate was 0.001.
- Experiment 2 resulted in more parameters (123,904 vs 111,872 for Exp 1) due to a larger vocabulary.
- The model learns to predict the next word by nudging its parameters to be less wrong during training.
- Evaluation success rates showed that trained models achieved 83.3% accuracy on the 48-case suite for Experiment 1.
- The model has a limitation in that it learns vocabulary and surface grammar but not reasoning.
- A proposed next experiment is to hold the corpus fixed and scale the training.

## Related concepts

- [[Learning Rate]] — It was set to 0.001 for both experiments.
- [[Corpus]] — Experiment 2 added 3 food/restaurant files to the baseline classroom sentences.
- [[Loss]] — Loss curves were tracked across different training steps for both experiments.
- [[Evaluation Suite]] — The corpus is used as study material for these evaluations.

## Sources

- Original: [[raw/custom-llm-readme.md]] (unchanged copy in `vault/raw/`)
