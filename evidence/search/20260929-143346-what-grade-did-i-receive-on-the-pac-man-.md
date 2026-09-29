# Search evidence card

- **Time:** 2026-09-29T14:33:46
- **Model:** `mlx-community/gemma-4-e2b-it-4bit`  ·  **Execution:** local  ·  **Mode:** search

## Question

What grade did I receive on the Pac-Man assignment?

## Retrieved passages

**** `wiki/Projects/Ms Pac-Man DQN Agent.md` — Ms Pac-Man DQN Agent (BM25 6.46)

> Assignment 2: a Deep Q-Network (DQN) agent that learns Ms. Pac-Man by trial and error from game pixels and score rewards. After tuning three hyperparameters over four runs, the trained agent's mean evaluation score rose from **492 to 1,072 (+118%)**, improving on all five evaluation seeds.

**** `wiki/Concepts/Exploration Rate.md` — Exploration Rate (BM25 5.2)

> In reinforcement learning, the fraction of moves the agent picks at random to try new things, instead of the move it currently thinks is best.
> 
> Appears in: - [[Ms Pac-Man DQN Agent]] — lowered 0.25 → 0.10 → 0.09, because random turns in Ms. Pac-Man often walk into ghosts.

**** `raw/pacman-dqn-readme.md` — Training a Ms. Pac-Man Agent (Deep Q-Network) > ⚙️ Hyperparameters (part 2) (BM25 4.16)

> Note that this run changed **two** settings from my previous one (exploration 0.10 → 0.09 and episodes 250 → 1000), so the improvement below cannot be attributed to the episode budget alone.
> 
> ---

**** `wiki/Concepts/Evaluation Suite.md` — Evaluation Suite > Appears in (BM25 4.16)

> - [[Custom nanoGPT LLM]] — a 48-case next-word exam with coverage, scorable accuracy and all-case success.
> - [[Ms Pac-Man DQN Agent]] — the same five seeds at 5% exploration, before and after training.

