---
type: source-note
source_id: pacman-dqn-readme
source_path: raw/pacman-dqn-readme.md
source_sha256: 5ad7c34b7ca2cf97
description: "This repository details the training of a Deep Q-Network (DQN) agent to play Ms"
generated_by: mlx-community/gemma-4-e2b-it-4bit
ingested: 2026-09-27
reviewed: false
---

# PacMan DQN Agent

This repository details the training of a Deep Q-Network (DQN) agent to play Ms. Pac-Man by learning through trial and error based on game pixels and score rewards. The training involved various hyperparameters and resulted in performance comparisons against an untrained network.

## Key details

- Exploration Rate was lowered across runs from 0.25 to 0.10 and finally to 0.09.
- The agent is evaluated at 5% exploration, and training near this value practices the behavior being graded.
- The agent observes the game as a stack of four consecutive 84x84 grayscale game screens to perceive movement and direction.
- The agent has 9 joystick moves available for action selection.
- Evaluation used fixed settings including five seeds, 5% exploration, and a 3,000-decision time limit.
- Training statistics showed 1,000 completed episodes and 594,907 total decisions.

## Related concepts

- [[Learning Rate]] — The rate at which the model updates its parameters is discussed in relation to learning updates in the experiment log.
- [[Loss]] — The concept is implied through the mention of "mean update loss" in the training dashboard visualization.
- [[Corpus]] — The game pixels are used as the input data for the agent, as the agent learns by observing these screens.
- [[Evaluation Suite]] — This suite was used to compare the performance of the trained network against the baseline untrained network.

## Sources

- Original: [[raw/pacman-dqn-readme.md]] (unchanged copy in `vault/raw/`)
