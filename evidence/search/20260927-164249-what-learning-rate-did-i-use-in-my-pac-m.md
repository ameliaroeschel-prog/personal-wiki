# Search evidence card

- **Time:** 2026-09-27T16:42:49
- **Model:** `mlx-community/gemma-4-e2b-it-4bit`  ·  **Execution:** local  ·  **Mode:** search

## Question

what learning rate did I use in my pac-man project?

## Retrieved passages

**** `wiki/Concepts/Exploration Rate.md` — Exploration Rate (BM25 9.94)

> In reinforcement learning, the fraction of moves the agent picks at random to try new things, instead of the move it currently thinks is best.
> 
> Appears in: - [[Ms Pac-Man DQN Agent]] — lowered 0.25 → 0.10 → 0.09, because random turns in Ms. Pac-Man often walk into ghosts.

**** `raw/pacman-dqn-readme.md` — Training a Ms. Pac-Man Agent (Deep Q-Network) > ⚙️ Hyperparameters (BM25 8.87)

> * **Exploration Rate:** `0.09` - I lowered exploration across my runs, from 0.25 to 0.10 and finally to 0.09. In Ms. Pac-Man a random turn often walks straight into a ghost, so a high random rate ends games early and the agent rarely sees the later part of a maze. The agent is also evaluated at 5% exploration, so training nearer that value practices the behavior being graded. I kept it above 5% so the agent still had some pressure to try alternatives, since exploration is fixed for the whole run rather than decaying.
> * **Episodes:** `1000` - My previous run's training scores were still trending upward when it ended at 250 episodes, which suggested the agent had not finished learning. Quadrupling the budget produced 148,477 learning updates instead of 37,419, and still finished in under 40 minutes on a Colab T4.
> * **Learning Rate:** `0.0001` - An earlier run at 0.0002 showed loss climbing while training scores fell, which suggested each update was too large for a replay memory holding only 5,000 decisions. At 0.0001 learning became steadier, so I held it fixed for my last two runs.

**** `wiki/Concepts/Learning Rate.md` — Learning Rate (BM25 8.7)

> The size of each weight update during training. Too large and training overshoots and loss climbs or diverges; too small and the model barely learns within the training budget.
> 
> Appears in: - [[Custom nanoGPT LLM]] — held at 0.001 for both experiments, with warmup and cosine decay.
> - [[Ms Pac-Man DQN Agent]] — lowered from 0.0002 to 0.0001 after loss climbed while scores fell.

**** `raw/pacman-dqn-readme.md` — Training a Ms. Pac-Man Agent (Deep Q-Network) > 📊 Evaluation & Scores > Experiment Log (part 2) (BM25 8.69)

> Run 1 was a five-episode setup check with only 539 learning updates, so its 730 reflects luck across five games rather than learning — a useful reminder of how noisy a five-game evaluation is. Run 2 trained 20× longer and scored worse, which is what prompted lowering both exploration and the learning rate. Runs 3 and 4 then improved steadily.
> 
> ---

