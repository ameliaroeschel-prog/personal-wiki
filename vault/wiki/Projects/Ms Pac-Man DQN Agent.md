---
type: source-note
source_id: pacman-dqn-readme
source_path: raw/pacman-dqn-readme.md
source_sha256: 5ad7c34b7ca2cf97
description: "Assignment 2: a Deep Q-Network trained to play Ms. Pac-Man; mean score 492 → 1072 after tuning three hyperparameters"
generated_by: mlx-community/gemma-4-e2b-it-4bit
ingested: 2026-09-27
reviewed: true
review_notes: "Renamed from 'Pacman DQN Agent'; added headline results, plateau and next experiment (Gemma's draft omitted them); section refs added."
---

# Ms Pac-Man DQN Agent

Assignment 2: a Deep Q-Network (DQN) agent that learns Ms. Pac-Man by trial and error from game pixels and score rewards. After tuning three hyperparameters over four runs, the trained agent's mean evaluation score rose from **492 to 1,072 (+118%)**, improving on all five evaluation seeds.

## Key details

- **Final settings:** exploration rate 0.09, 1,000 episodes, learning rate 0.0001 (§ Hyperparameters).
- Exploration was lowered 0.25 → 0.10 → 0.09 because random turns walk into ghosts; evaluation runs at 5% exploration (§ Hyperparameters).
- An earlier learning rate of 0.0002 showed loss climbing while scores fell; 0.0001 was steadier (§ Hyperparameters).
- The agent sees a stack of four 84×84 grayscale frames and chooses one of 9 joystick moves; rewards are clipped to −1…+1 during learning (§ How the Agent Works).
- Evaluation: same five seeds, 5% exploration, 3,000-decision limit, before and after training (§ Score Comparison).
- Trained on an NVIDIA T4 GPU in Google Colab: 594,907 decisions, 148,477 learning updates, 37.8 minutes (§ Training Statistics & Hardware).
- **Limitation:** learning plateaued after about episode 400; the likely cause is a replay memory of only 5,000 decisions (§ Limitations & Next Steps).
- **Next experiment:** raise replay memory from 5,000 to 50,000, holding the other settings fixed (§ Limitations & Next Steps).

## Related concepts

- [[Exploration Rate]] — the main dial tuned across runs; lowering it helped most.
- [[Learning Rate]] — halved to 0.0001 after loss climbed at 0.0002.
- [[Loss]] — mean update loss rose to ~0.12 then flattened, read as a settling agent.
- [[Replay Memory]] — the suspected cause of the plateau and the proposed next change.
- [[Evaluation Suite]] — fixed five-seed before/after evaluation makes runs comparable.

## Related projects

- [[Custom nanoGPT LLM]] — the other training experiment; both tune a learning rate and read loss curves.

## Sources

- Original: [[raw/pacman-dqn-readme.md]] (unchanged copy in `vault/raw/`)
