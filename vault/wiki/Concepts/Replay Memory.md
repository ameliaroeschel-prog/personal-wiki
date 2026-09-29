---
type: concept
description: "The buffer of recent decisions a DQN agent re-samples to learn from"
reviewed: true
---

# Replay Memory

A DQN agent stores its recent decisions and outcomes and trains on random samples from them. Its size limits how far back the agent can learn from.

## Related concepts

- [[Exploration Rate]] — determines what kind of experience fills the memory.

## Appears in

- [[Ms Pac-Man DQN Agent]] — held only 5,000 decisions (about eight games); the proposed next experiment raises it to 50,000.
