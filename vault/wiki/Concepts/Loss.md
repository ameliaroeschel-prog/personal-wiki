---
type: concept
description: "A number measuring how wrong the model's predictions are; training tries to push it down"
reviewed: true
---

# Loss

How far the model's predictions are from the targets. Falling loss means the model fits its training data better — but it is not the same as doing well on an evaluation.

## Related concepts

- [[Learning Rate]] — controls how quickly loss changes, and whether it becomes unstable.
- [[Evaluation Suite]] — the separate test that shows whether low loss translates into real performance.

## Appears in

- [[Custom nanoGPT LLM]] — plateaued around step 1,200; not comparable across different vocabularies.
- [[Ms Pac-Man DQN Agent]] — rose to about 0.12 then flattened; rising loss can mean the agent is finding bigger rewards.
