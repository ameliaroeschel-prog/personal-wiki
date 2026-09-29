---
type: concept
description: "How big a step the model takes each time it updates its weights"
reviewed: true
---

# Learning Rate

The size of each weight update during training. Too large and training overshoots and loss climbs or diverges; too small and the model barely learns within the training budget.

## Related concepts

- [[Loss]] — the signal that shows whether the learning rate is too high (loss climbs) or working (loss falls then settles).
- [[Exploration Rate]] — the other hyperparameter tuned in the Pac-Man runs.

## Appears in

- [[Custom nanoGPT LLM]] — held at 0.001 for both experiments, with warmup and cosine decay.
- [[Ms Pac-Man DQN Agent]] — lowered from 0.0002 to 0.0001 after loss climbed while scores fell.
