# Search evidence card

- **Time:** 2026-09-29T15:08:58
- **Model:** `mlx-community/gemma-4-e2b-it-4bit`  ·  **Execution:** local  ·  **Mode:** search

## Question

replay memory plateau

## Retrieved passages

**** `raw/pacman-dqn-readme.md` — Training a Ms. Pac-Man Agent (Deep Q-Network) > 🔬 Limitations & Next Steps (BM25 8.78)

> * **Observed Limitation:** Learning plateaued. After roughly episode 400 the 25-game average stopped trending upward, even though training continued for 600 more games, and the agent stayed inconsistent: its progress samples swing between 250 and 1,930 points on the same seed, and seed 202 scored 560 here against 850 in my shorter run. The likely cause is memory rather than practice. The agent remembers only its last 5,000 decisions, about eight games, so late in training it is still learning from a narrow slice of recent experience and cannot revisit the rare good games that would teach it the most. Watching the clips, it clears dots efficiently near where it starts but shows no sign of a plan for finishing a maze or for using power pellets to hunt ghosts.
> * **Next Experiment:** I would change only the **replay memory size**, from `5,000` to `50,000` decisions, keeping exploration at 0.09, episodes at 1,000, and the learning rate at 0.0001. The assignment allows tuning settings beyond the three main dials as long as the change is explained, and the plateau above points at memory as the binding constraint rather than the amount of play. A ten-times-larger memory would let the agent keep learning from roughly 80 past games instead of 8. I would expect the 25-game average to keep climbing past episode 400 instead of flattening, and I would watch whether the evaluation scores become less erratic across the five seeds.

**** `wiki/Concepts/Replay Memory.md` — Replay Memory (BM25 8.28)

> A DQN agent stores its recent decisions and outcomes and trains on random samples from them. Its size limits how far back the agent can learn from.
> 
> Appears in: - [[Ms Pac-Man DQN Agent]] — held only 5,000 decisions (about eight games); the proposed next experiment raises it to 50,000.

**** `wiki/Projects/Ms Pac-Man DQN Agent.md` — Ms Pac-Man DQN Agent > Key details (BM25 7.22)

> - **Final settings:** exploration rate 0.09, 1,000 episodes, learning rate 0.0001 (§ Hyperparameters).
> - Exploration was lowered 0.25 → 0.10 → 0.09 because random turns walk into ghosts; evaluation runs at 5% exploration (§ Hyperparameters).
> - An earlier learning rate of 0.0002 showed loss climbing while scores fell; 0.0001 was steadier (§ Hyperparameters).
> - The agent sees a stack of four 84×84 grayscale frames and chooses one of 9 joystick moves; rewards are clipped to −1…+1 during learning (§ How the Agent Works).
> - Evaluation: same five seeds, 5% exploration, 3,000-decision limit, before and after training (§ Score Comparison).
> - Trained on an NVIDIA T4 GPU in Google Colab: 594,907 decisions, 148,477 learning updates, 37.8 minutes (§ Training Statistics & Hardware).
> - **Limitation:** learning plateaued after about episode 400; the likely cause is a replay memory of only 5,000 decisions (§ Limitations & Next Steps).
> - **Next experiment:** raise replay memory from 5,000 to 50,000, holding the other settings fixed (§ Limitations & Next Steps).

