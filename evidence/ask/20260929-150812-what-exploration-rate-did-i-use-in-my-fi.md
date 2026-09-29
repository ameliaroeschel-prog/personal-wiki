# Ask evidence card

- **Time:** 2026-09-29T15:08:12
- **Model:** `mlx-community/gemma-4-e2b-it-4bit`  ·  **Execution:** local  ·  **Mode:** ask
- **Generation:** 2.17 s, peak memory 4.21 GB, 1112 prompt tokens

## Question

What exploration rate did I use in my final Pac-Man run?

## Retrieved passages

**S1** `raw/pacman-dqn-readme.md` — Training a Ms. Pac-Man Agent (Deep Q-Network) > ⚙️ Hyperparameters (BM25 12.91)

> * **Exploration Rate:** `0.09` - I lowered exploration across my runs, from 0.25 to 0.10 and finally to 0.09. In Ms. Pac-Man a random turn often walks straight into a ghost, so a high random rate ends games early and the agent rarely sees the later part of a maze. The agent is also evaluated at 5% exploration, so training nearer that value practices the behavior being graded. I kept it above 5% so the agent still had some pressure to try alternatives, since exploration is fixed for the whole run rather than decaying.
> * **Episodes:** `1000` - My previous run's training scores were still trending upward when it ended at 250 episodes, which suggested the agent had not finished learning. Quadrupling the budget produced 148,477 learning updates instead of 37,419, and still finished in under 40 minutes on a Colab T4.
> * **Learning Rate:** `0.0001` - An earlier run at 0.0002 showed loss climbing while training scores fell, which suggested each update was too large for a replay memory holding only 5,000 decisions. At 0.0001 learning became steadier, so I held it fixed for my last two runs.

**S2** `wiki/Concepts/Exploration Rate.md` — Exploration Rate (BM25 11.9)

> In reinforcement learning, the fraction of moves the agent picks at random to try new things, instead of the move it currently thinks is best.
> 
> Appears in: - [[Ms Pac-Man DQN Agent]] — lowered 0.25 → 0.10 → 0.09, because random turns in Ms. Pac-Man often walk into ghosts.

**S3** `wiki/Projects/Ms Pac-Man DQN Agent.md` — Ms Pac-Man DQN Agent > Key details (BM25 11.66)

> - **Final settings:** exploration rate 0.09, 1,000 episodes, learning rate 0.0001 (§ Hyperparameters).
> - Exploration was lowered 0.25 → 0.10 → 0.09 because random turns walk into ghosts; evaluation runs at 5% exploration (§ Hyperparameters).
> - An earlier learning rate of 0.0002 showed loss climbing while scores fell; 0.0001 was steadier (§ Hyperparameters).
> - The agent sees a stack of four 84×84 grayscale frames and chooses one of 9 joystick moves; rewards are clipped to −1…+1 during learning (§ How the Agent Works).
> - Evaluation: same five seeds, 5% exploration, 3,000-decision limit, before and after training (§ Score Comparison).
> - Trained on an NVIDIA T4 GPU in Google Colab: 594,907 decisions, 148,477 learning updates, 37.8 minutes (§ Training Statistics & Hardware).
> - **Limitation:** learning plateaued after about episode 400; the likely cause is a replay memory of only 5,000 decisions (§ Limitations & Next Steps).
> - **Next experiment:** raise replay memory from 5,000 to 50,000, holding the other settings fixed (§ Limitations & Next Steps).

**S4** `raw/pacman-dqn-readme.md` — Training a Ms. Pac-Man Agent (Deep Q-Network) > 📊 Evaluation & Scores > Experiment Log (part 2) (BM25 11.55)

> Run 1 was a five-episode setup check with only 539 learning updates, so its 730 reflects luck across five games rather than learning — a useful reminder of how noisy a five-game evaluation is. Run 2 trained 20× longer and scored worse, which is what prompted lowering both exploration and the learning rate. Runs 3 and 4 then improved steadily.
> 
> ---

## Answer

The exploration rate used in the final settings was $0.09$ [S3].

## Citation check

- Cited: ['S3']
- Invalid (not retrieved): none
- Verdict: ok: all citations point to retrieved passages (still verify they support the claims)

