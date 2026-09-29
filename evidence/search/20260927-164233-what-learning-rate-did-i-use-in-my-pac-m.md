# Search evidence card

- **Time:** 2026-09-27T16:42:33
- **Model:** `mlx-community/gemma-4-e2b-it-4bit`  ·  **Execution:** local  ·  **Mode:** search

## Question

what learning rate did I use in my pac-man project?

## Retrieved passages

**** `wiki/Projects/Custom nanoGPT LLM.md` — Custom nanoGPT LLM > Related projects (BM25 12.19)

> - [[Ms Pac-Man DQN Agent]] — the other training experiment; both tune a learning rate and read loss curves.

**** `wiki/Projects/Ms Pac-Man DQN Agent.md` — Ms Pac-Man DQN Agent > Related projects (BM25 12.19)

> - [[Custom nanoGPT LLM]] — the other training experiment; both tune a learning rate and read loss curves.

**** `wiki/Concepts/Learning Rate.md` — Learning Rate > Related concepts (BM25 10.11)

> - [[Loss]] — the signal that shows whether the learning rate is too high (loss climbs) or working (loss falls then settles).
> - [[Exploration Rate]] — the other hyperparameter tuned in the Pac-Man runs.

**** `wiki/Concepts/Learning Rate.md` — Learning Rate > Appears in (BM25 8.31)

> - [[Custom nanoGPT LLM]] — held at 0.001 for both experiments, with warmup and cosine decay.
> - [[Ms Pac-Man DQN Agent]] — lowered from 0.0002 to 0.0001 after loss climbed while scores fell.

**** `wiki/Concepts/Exploration Rate.md` — Exploration Rate > Appears in (BM25 7.7)

> - [[Ms Pac-Man DQN Agent]] — lowered 0.25 → 0.10 → 0.09, because random turns in Ms. Pac-Man often walk into ghosts.

