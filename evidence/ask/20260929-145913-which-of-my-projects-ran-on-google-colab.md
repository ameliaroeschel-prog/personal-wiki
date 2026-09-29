# Ask evidence card

- **Time:** 2026-09-29T14:59:13
- **Model:** `mlx-community/gemma-4-e2b-it-4bit`  ·  **Execution:** local  ·  **Mode:** ask
- **Generation:** 4.02 s, peak memory 4.21 GB, 1117 prompt tokens

## Question

Which of my projects ran on Google Colab, and what hardware did each use?

## Retrieved passages

**S1** `raw/pacman-dqn-readme.md` — Training a Ms. Pac-Man Agent (Deep Q-Network) > 📈 Training Statistics & Hardware (BM25 10.88)

> * **Run status:** Completed (not interrupted). Run ID `20260915_231634_675837`.
> * **Hardware Used:** NVIDIA T4 GPU (CUDA) via Google Colab. Exact Python and package versions are recorded in [config.json](results/config.json).
> * **Completed Episodes:** 1,000 of 1,000
> * **Total Decisions (Steps):** 594,907
> * **Total Learning Updates:** 148,477
> * **Elapsed Training Time:** 2,265 seconds (37.8 minutes, including the periodic gameplay samples)
> * **Best single training game:** 4,020 points
> 
> Source: [training_summary.json](results/training_summary.json)
> 
> ---

**S2** `raw/custom-llm-readme.md` — Building a Custom LLM — Class 4 Assignment > 1. Overview & how to run (part 2) (BM25 8.2)

> **To run it yourself:** open either notebook in Google Colab (default free CPU is enough) or locally with `pip install -r requirements.txt` and Jupyter. Set the three choices in **Section 1**, then **Runtime → Run all**. For Experiment 2, upload the three `corpus/*.txt` files into Colab's `corpus/` folder *before* Run all (keep `CORPUS = "classroom"` so they're **added** to the classroom sentences).
> 
> ---

**S3** `raw/custom-llm-readme.md` — Building a Custom LLM — Class 4 Assignment > 4. Run facts (BM25 7.23)

> | | Exp 1 | Exp 2 |
> |---|---|---|
> | Completed steps | 3,000 (not interrupted) | 3,000 (not interrupted) |
> | Elapsed time | 38.9 s | 52.3 s |
> | Hardware | Colab CPU (Linux x86_64, PyTorch 2.11 CPU) | same |
> | Parameters | 111,872 | 123,904 |
> | Vocabulary | 136 | 324 |
> 
> *(Exp 2 has more parameters only because a larger vocabulary means a larger embedding table — the network architecture is identical.)*
> 
> ---

**S4** `wiki/Projects/Ms Pac-Man DQN Agent.md` — Ms Pac-Man DQN Agent > Key details (BM25 7.17)

> - **Final settings:** exploration rate 0.09, 1,000 episodes, learning rate 0.0001 (§ Hyperparameters).
> - Exploration was lowered 0.25 → 0.10 → 0.09 because random turns walk into ghosts; evaluation runs at 5% exploration (§ Hyperparameters).
> - An earlier learning rate of 0.0002 showed loss climbing while scores fell; 0.0001 was steadier (§ Hyperparameters).
> - The agent sees a stack of four 84×84 grayscale frames and chooses one of 9 joystick moves; rewards are clipped to −1…+1 during learning (§ How the Agent Works).
> - Evaluation: same five seeds, 5% exploration, 3,000-decision limit, before and after training (§ Score Comparison).
> - Trained on an NVIDIA T4 GPU in Google Colab: 594,907 decisions, 148,477 learning updates, 37.8 minutes (§ Training Statistics & Hardware).
> - **Limitation:** learning plateaued after about episode 400; the likely cause is a replay memory of only 5,000 decisions (§ Limitations & Next Steps).
> - **Next experiment:** raise replay memory from 5,000 to 50,000, holding the other settings fixed (§ Limitations & Next Steps).

## Answer

*   **Ms Pac-Man DQN Agent:** Trained on an NVIDIA T4 GPU via Google Colab [S1], and also trained on an NVIDIA T4 GPU in Google Colab [S4].
*   **Custom LLM (Experiment 1 and 2):** Used Colab CPU (Linux x86\_64, PyTorch 2.11 CPU) for both experiments [S3].

## Citation check

- Cited: ['S1', 'S3', 'S4']
- Invalid (not retrieved): none
- Verdict: ok: all citations point to retrieved passages (still verify they support the claims)

