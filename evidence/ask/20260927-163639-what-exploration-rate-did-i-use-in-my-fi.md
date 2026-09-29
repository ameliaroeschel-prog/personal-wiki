# Ask evidence card

- **Time:** 2026-09-27T16:36:39
- **Model:** `mlx-community/gemma-4-e2b-it-4bit`  ·  **Execution:** local  ·  **Mode:** ask
- **Generation:** 3.22 s, peak memory 4.2 GB, 1093 prompt tokens

## Question

What exploration rate did I use in my final Pac-Man run?

## Retrieved passages

**S1** `raw/pacman-dqn-readme.md` — Training a Ms. Pac-Man Agent (Deep Q-Network) > ⚙️ Hyperparameters (BM25 12.71)

> * **Exploration Rate:** `0.09` - I lowered exploration across my runs, from 0.25 to 0.10 and finally to 0.09. In Ms. Pac-Man a random turn often walks straight into a ghost, so a high random rate ends games early and the agent rarely sees the later part of a maze. The agent is also evaluated at 5% exploration, so training nearer that value practices the behavior being graded. I kept it above 5% so the agent still had some pressure to try alternatives, since exploration is fixed for the whole run rather than decaying.
> * **Episodes:** `1000` - My previous run's training scores were still trending upward when it ended at 250 episodes, which suggested the agent had not finished learning. Quadrupling the budget produced 148,477 learning updates instead of 37,419, and still finished in under 40 minutes on a Colab T4.
> * **Learning Rate:** `0.0001` - An earlier run at 0.0002 showed loss climbing while training scores fell, which suggested each update was too large for a replay memory holding only 5,000 decisions. At 0.0001 learning became steadier, so I held it fixed for my last two runs.

**S2** `raw/pacman-dqn-readme.md` — Training a Ms. Pac-Man Agent (Deep Q-Network) > 📊 Evaluation & Scores > Experiment Log (part 2) (BM25 11.24)

> Run 1 was a five-episode setup check with only 539 learning updates, so its 730 reflects luck across five games rather than learning — a useful reminder of how noisy a five-game evaluation is. Run 2 trained 20× longer and scored worse, which is what prompted lowering both exploration and the learning rate. Runs 3 and 4 then improved steadily.
> 
> ---

**S3** `raw/pacman-dqn-readme.md` — Training a Ms. Pac-Man Agent (Deep Q-Network) > ⚙️ Hyperparameters (part 2) (BM25 9.49)

> Note that this run changed **two** settings from my previous one (exploration 0.10 → 0.09 and episodes 250 → 1000), so the improvement below cannot be attributed to the episode budget alone.
> 
> ---

**S4** `raw/pacman-dqn-readme.md` — Training a Ms. Pac-Man Agent (Deep Q-Network) > 📊 Evaluation & Scores > Experiment Log (BM25 9.28)

> All four runs used identical evaluation settings, so their trained means are directly comparable. The baseline is the same every time because the starting weights come from a fixed seed.
> 
> | Run | Exploration | Episodes | Learning rate | Learning updates | Baseline mean | Trained mean |
> | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
> | 1 (setup check) | 0.25 | 5 | 0.0002 | 539 | 492.0 | 730.0 |
> | 2 | 0.25 | 100 | 0.0002 | 14,706 | 492.0 | 534.0 |
> | 3 | 0.10 | 250 | 0.0001 | 37,419 | 492.0 | 664.0 |
> | **4 (submitted)** | **0.09** | **1000** | **0.0001** | **148,477** | **492.0** | **1072.0** |

## Answer

The exploration rate used in the final run was $0.09$ [S4].

## Citation check

- Cited: ['S4']
- Invalid (not retrieved): none
- Verdict: ok: all citations point to retrieved passages (still verify they support the claims)

