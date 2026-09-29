# Ask-mode test set (answer key — kept OUTSIDE vault/ so retrieval can never see it)

Written 2026-09-27, before `ask` mode or ingestion were built. Only the BM25 search had been run at that point.
Each test runs with `./wiki ask "<question>" --mode local`. Every ask is standalone: no chat history.

## Test 1: direct, one source
- **Question:** What exploration rate did I use in my final Pac-Man run?
- **Expected answer:** 0.09 (lowered from 0.25 → 0.10 → 0.09).
- **Expected source:** `vault/raw/pacman-dqn-readme.md`, section *⚙️ Hyperparameters*:
  > **Exploration Rate:** `0.09` - I lowered exploration across my runs, from 0.25 to 0.10 and finally to 0.09.
- **Pass if:** the answer says 0.09 and cites a passage that contains it.

## Test 2: paraphrased wording
- **Question:** How much bigger did the word list get when I added the food files?
- **Why it's hard:** the source says "vocabulary", not "word list". This checks whether keyword retrieval copes with different wording.
- **Expected answer:** vocabulary grew from 136 to 324 words (+188).
- **Expected source:** `vault/raw/custom-llm-readme.md`, section *Corpus details*:
  > **Vocabulary:** grew from **136 → 324 words**.
- **Pass if:** 136 → 324 is stated and cited to a passage that contains it.

## Test 3: connects two sources
- **Question:** Which of my projects ran on Google Colab, and what hardware did each use?
- **Expected answer:** Ms. Pac-Man DQN ran on an NVIDIA T4 GPU in Colab. The custom nanoGPT LLM ran on Colab CPU.
- **Expected sources:**
  - `vault/raw/pacman-dqn-readme.md`, *📈 Training Statistics & Hardware*: "NVIDIA T4 GPU (CUDA) via Google Colab"
  - `vault/raw/custom-llm-readme.md`, *4. Run facts*: "Colab CPU (Linux x86_64, PyTorch 2.11 CPU)"
- **Pass if:** both projects appear with the correct hardware, each cited to its own source. Naming only one is a partial pass.

## Test 4: unanswerable
- **Question:** What grade did I receive on the Pac-Man assignment?
- **Expected behavior:** `INSUFFICIENT EVIDENCE`. No source mentions a grade (checked with `grep -ri grade vault/raw`, which only finds "the behavior being graded"; the networking README has a "Grading evidence" section, but it lists test proofs, not a grade).
- **Fail if:** it invents a grade or cites a passage as if it gave one.
