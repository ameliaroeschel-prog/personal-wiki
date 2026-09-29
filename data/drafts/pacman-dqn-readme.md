---
type: source-note
source_id: pacman-dqn-readme
source_path: raw/pacman-dqn-readme.md
source_sha256: 5ad7c34b7ca2cf97
description: "This document details the training of a Deep Q-Network (DQN) agent to play Ms"
generated_by: mlx-community/gemma-4-e2b-it-4bit
ingested: 2026-09-29
reviewed: false
---

# Pacman DQN Agent

This document details the training of a Deep Q-Network (DQN) agent to play Ms. Pac-Man by learning through trial and error based on game pixels and score rewards. The training involved tuning hyperparameters, observing performance metrics, and noting limitations related to memory.

## Key details

- Exploration Rate was lowered from 0.25 to 0.10 and finally to 0.09.
- The agent is evaluated at 5% exploration, and training near this value practices the behavior being graded.
- The agent observes the game as a stack of four consecutive 84x84 grayscale game screens to perceive movement.
- The agent has 9 joystick moves available for action selection.
- Training statistics show 594,907 total decisions and 148,477 total learning updates.
- A limitation observed was that the learning plateaued after roughly episode 400, and progress samples swung between 250 and 1,930 points on the same seed.

## Related concepts

- [[Exploration Rate]] — This parameter controls how much randomness is allowed in the agent's actions during training.
- [[Learning Rate]] — This parameter dictates the magnitude of updates applied to the network during the training process.
- [[Loss]] — This term is referenced in the context of learning updates, indicating the error signal used to guide the network's adjustments.

## Sources

- Original: [[raw/pacman-dqn-readme.md]] (unchanged copy in `vault/raw/`)
