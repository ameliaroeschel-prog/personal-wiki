---
type: concept
description: "How often a reinforcement-learning agent takes a random action instead of its best guess"
reviewed: true
---

# Exploration Rate

In reinforcement learning, the fraction of moves the agent picks at random to try new things, instead of the move it currently thinks is best.

## Related concepts

- [[Learning Rate]] — the other hyperparameter tuned alongside it.
- [[Replay Memory]] — what the agent learns from; exploration decides what goes into it.

## Appears in

- [[Ms Pac-Man DQN Agent]] — lowered 0.25 → 0.10 → 0.09, because random turns in Ms. Pac-Man often walk into ghosts.
