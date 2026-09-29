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

# Pacman DQN Agent

This repository details the training of a Deep Q-Network (DQN) agent to play Ms. Pac-Man by observing game pixels and receiving score rewards. The agent learns through trial and error by interacting with the game environment.

## Key details

- Exploration Rate was lowered from 0.25 to 0.10 and finally to 0.09.
- The agent is evaluated at 5% exploration, and training near this value practices the behavior being graded.
- The agent observes the game as a stack of four consecutive 84x84 grayscale game screens to perceive movement and direction.
- The agent has 9 joystick moves available: NOOP, UP, RIGHT, LEFT, DOWN, UPRIGHT, UPLEFT, DOWNRIGHT, and DOWNLEFT.
- Training statistics show 594,907 total decisions and 148,477 learning updates.
- The training run completed with 1,000 of 1,000 episodes, using an NVIDIA T4 GPU via Google Colab.

## Related concepts

- [[Exploration Rate]] — This parameter controls how much randomness is allowed in the agent's actions.
- [[Observations]] — This refers to the input the agent uses to perceive the game state.
- [[Learning Rate]] — This parameter is recorded in the experiment log and dictates the magnitude of learning updates.
- [[Loss]] — This term is mentioned in the context of learning updates, indicating the error being minimized during training.

## Sources

- Original: [[raw/pacman-dqn-readme.md]] (unchanged copy in `vault/raw/`)
