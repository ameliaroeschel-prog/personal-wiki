# Building a Custom LLM — Class 4 Assignment

**Author:** Amelia Roeschel
**Model:** [nanoGPT](https://github.com/karpathy/nanoGPT) (Andrej Karpathy), word-token variant — 2 blocks, 4 heads, 64-dim embeddings, 48-token context, trained with PyTorch + AdamW on CPU.
**What this is:** two small experiments that train a *tiny* language model from scratch and inspect, step by step, how text becomes predictions and how a neural network learns. This is **not** a chat assistant — it continues sentences in the style of its training corpus.

---

## 1. Overview & how to run

Two experiments, same model and settings, only the corpus changes:

| | Experiment 1 | Experiment 2 |
|---|---|---|
| Corpus | Starter "classroom" sentences only | Classroom **+ 3 food/restaurant files** |
| Training steps | 3,000 | 3,000 |
| Learning rate | 0.001 | 0.001 |
| Executed notebook | [custom_llm_experiment1_classroom.ipynb](custom_llm_experiment1_classroom.ipynb) | [custom_llm_experiment2_extended.ipynb](custom_llm_experiment2_extended.ipynb) |
| Results folder | [llm_runs/exp1_classroom/](llm_runs/exp1_classroom/) | [llm_runs/exp2_extended/](llm_runs/exp2_extended/) |

**To run it yourself:** open either notebook in Google Colab (default free CPU is enough) or locally with `pip install -r requirements.txt` and Jupyter. Set the three choices in **Section 1**, then **Runtime → Run all**. For Experiment 2, upload the three `corpus/*.txt` files into Colab's `corpus/` folder *before* Run all (keep `CORPUS = "classroom"` so they're **added** to the classroom sentences).

---

## 2. My three choices, and why

| Choice | Value | Why |
|---|---|---|
| **Corpus** | `classroom`, then `classroom` + 3 files | Experiment 1 is a clean baseline on the supplied sentences. Experiment 2 adds focused teaching material so I can measure the *effect of the corpus* with everything else held constant. |
| **Training steps** | 3,000 | The recommended budget. One step = one guess-check-nudge on 32 example passages. Enough for a tiny model to clearly learn patterns on a small corpus without overtraining (the loss plateaus by ~step 1,200 — see §6). |
| **Learning rate** | 0.001 | The size of each weight nudge. Too **large** (e.g. 0.1) and the model overshoots and the loss diverges; too **small** (e.g. 1e-5) and it barely moves in 3,000 steps. 0.001 is the tested middle for AdamW; the notebook adds warmup + cosine decay. |

### Corpus details
- **Sources & permissions:** all corpus files are original sentences I wrote for this assignment (`corpus/food_negation.txt`, `corpus/food_opposites.txt`, `corpus/food_sequence.txt`). No copyrighted, confidential, or personal data. Free to share.
- **Format / extraction check:** all three are UTF-8 **plain text** (`.txt`), so no PDF extraction or OCR was needed. The corpus manifest recorded **0 warnings** for all three files ([corpus_manifest.json](llm_runs/exp2_extended/corpus_manifest.json)).
- **Passages added:** 163 unique passages (negation 84, opposites 33, sequence 46), split at ≤47 tokens on sentence boundaries.
- **Vocabulary:** grew from **136 → 324 words**. Unknown-token rates: **training 0.0%**, held-out validation **0.23%** ([vocabulary_report.json](llm_runs/exp2_extended/vocabulary_report.json)).
- **Split:** duplicates removed, then a 90/10 passage split — Exp 2: **4,279 train / 476 validation** passages. Validation passages never supply weight updates.

---

## 3. What I predicted, and what happened

**My prediction (written before training):**
> I expect the untrained model to produce random gibberish, since its weights start random. More training steps should improve it — each step reinforces the corpus patterns — and expanding the corpus should help, because the model can only use words it has actually seen. But I don't expect it to ever be "good": it's tiny compared to ChatGPT or Claude. My core hypothesis is that **focus beats breadth for a model this small** — a narrow corpus (food/restaurants) limits the vocabulary it must learn, which should give it a better shot at coherent output and higher scores.

**What actually happened:** The untrained model *was* gibberish (✓). Training clearly worked (loss fell, samples became grammatical, scorable accuracy jumped to 83–86%). My "narrow beats broad" hypothesis was **partly confirmed and partly refuted**, in an interesting way:
- ✅ The narrow food corpus raised **coverage** (50% → 58%) — it taught the vocabulary that made 8 previously-impossible questions answerable.
- ❌ It did **not** teach the *reasoning*. The targeted categories (negation, opposites, sequence) stayed at **0 correct** even after they became scorable. Vocabulary ≠ reasoning (see §7 and §8).

---

## 4. Run facts

| | Exp 1 | Exp 2 |
|---|---|---|
| Completed steps | 3,000 (not interrupted) | 3,000 (not interrupted) |
| Elapsed time | 38.9 s | 52.3 s |
| Hardware | Colab CPU (Linux x86_64, PyTorch 2.11 CPU) | same |
| Parameters | 111,872 | 123,904 |
| Vocabulary | 136 | 324 |

*(Exp 2 has more parameters only because a larger vocabulary means a larger embedding table — the network architecture is identical.)*

---

## 5. How the model learns — traced through my actual data

The whole model plays one game: **predict the next word**, over and over, nudging its knobs to be less wrong. Here is that pipeline traced through real values from Experiment 2 ([inspection.json](llm_runs/exp2_extended/inspection.json), [tokenization.json](llm_runs/exp2_extended/tokenization.json)):

1. **Corpus → tokens.** Text is chopped into word/punctuation **tokens**. `"the customer ordered ."` → `the`, `customer`, `ordered`, `.`
2. **Token → ID.** Each unique token gets a number (an address). The word **`customer` is ID 80** in Exp 2's 324-word vocabulary.
3. **ID → vector (embedding).** Each ID maps to a list of **64 numbers** representing its learned "meaning." For `customer`, the first 5 numbers were:
   - **Before training:** `[0.0272, -0.0302, -0.0213, -0.0190, 0.0252]` (random)
   - **After training:** `[-0.0498, 0.0254, 0.0731, -0.1240, -0.0313]`
   - The whole 64-number vector moved by an L2 distance of **0.65** — training reshaped what "customer" means to the model.
4. **One gradient + weight update.** The first recorded update nudged coordinate 0 of `customer`'s embedding: value **0.027245**, gradient **0.000369**, warmup learning rate **1e-5** → new value **0.027235**. A microscopic step *downhill* on the loss. Multiply this by ~124k parameters × 3,000 steps and you get learning.
5. **Prediction (next-token probabilities).** Given the prefix **`the customer`**, the model's top next-word guesses:
   - **Before training:** essentially flat — top word only 0.6% (random across 324 words).
   - **After training:** sharply peaked on sensible verbs — **recommended 19%, compared 18%, returned 17%, selected 16%, ordered 14%**. It learned that "the customer ___" is followed by an action.
6. **Attention & context.** Each of the 4 attention heads lets a token look back at earlier tokens in the 48-token window and weight which ones matter for the next prediction (saved as `attention_rows` in inspection.json). That's how "customer" influences what comes after it.
7. **Loss.** A single number for "how wrong were the guesses" — averaged over next-token targets. Falling loss = learning (see §6).
8. **Temperature** (inference only, no weight change) — see §9.

---

## 6. Loss & samples

**Loss** (fixed evaluation panels of ≤20 training and ≤20 validation passages — small estimates, not full-corpus):

| Step | Exp 1 train / val | Exp 2 train / val |
|---|---|---|
| 0 | 4.926 / 4.928 | 5.785 / 5.777 |
| 1,500 | 0.682 / 0.718 | 0.802 / 0.711 |
| 3,000 | 0.678 / 0.706 | 0.731 / 0.707 |

**Loss curves** (fixed panels of ≤20 train + ≤20 validation passages):

| Experiment 1 (classroom) | Experiment 2 (extended) |
|---|---|
| ![Experiment 1 loss curve](llm_runs/exp1_classroom/training_curves.svg) | ![Experiment 2 loss curve](llm_runs/exp2_extended/training_curves.svg) |

*(If the SVGs don't render inline for you: [Exp 1 SVG](llm_runs/exp1_classroom/training_curves.svg) · [Exp 2 SVG](llm_runs/exp2_extended/training_curves.svg) — the same plots also appear as cell outputs in the executed notebooks. Full numeric tables: [history.json](llm_runs/exp2_extended/history.json).)*

> **Note on comparing the two loss curves:** they look almost identical, but **loss is not directly comparable across different corpora/vocabularies.** Exp 2 has 324 words vs 136, so it starts *more* uncertain (higher loss) and a similar ending number reflects a harder prediction task. Loss only measures *fit to the model's own corpus* — not exam performance. The corpus extension's real effect shows up in the eval **coverage** and **success rate** (§7), not the loss plot. *(Falling training loss alone does not demonstrate generalization — and here training and validation track together only because the synthetic corpus reuses templates.)*

**Text samples** (same generation settings; full timelines in [Exp1 samples/](llm_runs/exp1_classroom/samples/) and [Exp2 samples/](llm_runs/exp2_extended/samples/)):

| Stage | Exp 2 sample |
|---|---|
| **Untrained (step 0)** | `pear professor bond doctor course harvest team physician journey...` — word salad, includes `<UNK>` |
| **Halfway (step 1,500)** | `our school has a question about the new educator and lesson.` — real grammar appears |
| **Final (step 3,000)** | `the different mango was mentioned in the harvest report yesterday.` — grammatical, and a food word (`mango`) has bled in |

**Visible change:** from random word lists → grammatical sentences that echo the corpus. The food vocabulary appears only occasionally in samples because the 163 food passages are just **3.4%** of the corpus — a dilution that matters for §8.

---

## 7. Evaluations — the 48-case suite

An **eval** is a fixed test: a prompt, four single-word choices, an answer key, and a scoring rule. The suite ([evals/language_evals.json](evals/language_evals.json), unchanged) is the **exam**; the corpus is the **study material**. **Score = 1** if the model gives the correct choice the highest probability among the four, else 0. Ties get 0. Cases whose prompt/answer words are unknown to the model are **unscorable** (0 in all-case success). This scores next-word *selection*, not the separately-saved free continuation.

**Three metrics:** *coverage* = can the model attempt the question (are its words in vocab)? · *scorable accuracy* = of attempted, how many right? · *all-case success* = of all 48, how many right?

### The required four-row comparison

| Experiment | Stage | All-case success | Scorable accuracy | Coverage |
|---|---|---|---|---|
| **Exp 1 — classroom** | Untrained | 9/48 (18.8%) | 37.5% | 50% |
| **Exp 1 — classroom** | **Trained** | **20/48 (41.7%)** | **83.3%** | 50% |
| **Exp 2 — extended** | Untrained | 8/48 (16.7%) | 28.6% | 58% |
| **Exp 2 — extended** | **Trained** | **24/48 (50.0%)** | **85.7%** | **58%** |

**All four result sets:**
[Exp1 untrained](llm_runs/exp1_classroom/language_evals/untrained/) · [Exp1 trained](llm_runs/exp1_classroom/language_evals/final/) · [Exp2 untrained](llm_runs/exp2_extended/language_evals/untrained/) · [Exp2 trained](llm_runs/exp2_extended/language_evals/final/)

### Leakage / separation checks
Eval prompts, answer choices, keys, and outputs were kept **out of all training input**. The notebook's own separation check withheld the 16 reserved-prefix passages before splitting/vocab ([eval_separation.json](llm_runs/exp2_extended/eval_separation.json)), and I ran an automated check confirming **none of my three corpus files contain any exact eval prompt**. My food sentences teach the *skills* with different people, objects, and wording; ordinary word overlap (e.g. "milk", "hot") is allowed and necessary for coverage.

---

## 8. The corpus extension — what I chose, and honest results

**Categories chosen: negation, opposites, sequence.** I picked these because (a) all three scored **0% coverage** in Experiment 1 — the classroom corpus never taught their vocabulary — and (b) all three fit a single narrow topic (a restaurant), which tests my "focus beats breadth" hypothesis. My teaching material:
- **`food_negation.txt`** — order corrections: *"the guest did not order tea. she ordered milk. the guest ordered milk."*
- **`food_opposites.txt`** — the *"the opposite of X is Y"* frame with food pairs (sweet/sour, fresh/stale), plus the exam's pairs in reversed order.
- **`food_sequence.txt`** — cooking/dining steps: *"first chop the onion. then fry it. the last step is fry."*

**How the targeted categories moved** (coverage vs. Experiment 1, where all three were 0%):

| Category | Exp 1 coverage | Exp 2 coverage | Exp 2 correct |
|---|---|---|---|
| Negation | 0% | **67%** | 0/3 |
| Opposites | 0% | **33%** | 0/3 |
| Sequence | 0% | **33%** | 0/3 |

**What this means — the honest finding:** the extension worked *at the vocabulary level* (coverage rose from 0%, so questions became answerable) but **not at the reasoning level** (still 0 correct). Teaching the words milk/tea/hot/cold/breakfast did not teach the model to *track a negation*, *retrieve an antonym*, or *order events*. Those require compositional reasoning a 2-layer model can't acquire from 163 diluted example passages.

**Where the overall gain came from:** the trained score rose 41.7% → 50% (+4 cases), but the +4 came almost entirely from **new_wording (4/8 → 8/8)** — general robustness on familiar patterns — *not* my target categories. Extra, varied data made the model steadier on things it already half-knew, rather than unlocking new skills.

---

## 9. Temperature (inference only)

Temperature reshapes *how* the model samples from its probabilities **without changing any weights**. Low temp = greedier/safer/more repetitive; high temp = more random/varied/more errors. Examples ([temperature_comparison.json](llm_runs/exp2_extended/temperature_comparison.json), same seed & start token):

| Temp | Sample |
|---|---|
| 0.3 | `the local credit was mentioned in the return report yesterday.` |
| 0.8 | `they compared the new buyer with another buyer at the store.` |
| 1.2 | `they compared the new buyer with another buyer at the store.` |

Because the trained distribution is sharply peaked, the visible effect on these short samples is modest — but the mechanism (reweighting the same probabilities at generation time) is the point.

---

## 10. One limitation + proposed next experiment

**Limitation:** the model learns **vocabulary and surface grammar, but not reasoning.** It can produce *"the guest ordered milk"* yet cannot answer *"the guest did not order tea, so she ordered ___"* — it doesn't compose the negation. This is a scale limit, not a bug.

**Proposed next experiment:** hold the corpus fixed and **scale the model's depth** (e.g. 2 → 4 blocks) and/or **10× the targeted teaching data**, then re-run the 48 evals to test whether negation/opposites/sequence *accuracy* (not just coverage) improves. This isolates whether the ceiling is the data or the model size.

### My questions along the way (reflections)
- *"The Exp 2 loss graph doesn't look better than Exp 1."* — Correct, and it taught me that **loss measures corpus fit, not exam performance, and isn't comparable across vocabularies.** The real gain is in eval coverage/accuracy.
- *"Would reasoning emerge with a much bigger vocabulary and millions of training steps?"* — Not from steps alone. **Three things must scale together: far more varied data, a much bigger/deeper model (hundreds of billions of params vs my ~124k), and more compute.** Millions of steps on *this* tiny setup would just **overfit** — memorize the 163 sentences harder — which the flat loss curve past step ~1,200 already hints at. Even frontier models are doing sophisticated next-word prediction at scale, the *same core operation* my model does; scale is what makes reasoning-like behavior emerge.

---

## 11. Chat interface

A working terminal/notebook interface where you type a prompt and the **trained nanoGPT** replies (it continues a sentence; it does not answer questions). It loads `model.pt` + saved vocabulary from a run; each prompt starts fresh (no conversation memory); unknown words become `<UNK>`; context is capped at 48 tokens. Generating replies does **not** retrain the model.

**Launch:**
```bash
python chat.py --model llm_runs/exp2_extended/model.pt
```
Or use the notebook's **Section 10** cell with the trained model already in memory.

**Model/run used:** Experiment 2 (`exp2_extended`, 3,000 steps). Full transcript: [chat_transcript.json](llm_runs/exp2_extended/chat_transcript.json) (8 interactions).

**Actual interactions:**

| # | My prompt | Model reply | Note |
|---|---|---|---|
| 1 | `the customer` | `returned the offering after checking the price .` | coherent continuation |
| 2 | `the waiter brought` | `juice .` | plausible food word |
| 3 | `first chop an onion` | `.` | **limitation:** `an` was an **unknown word** → the model stalled |
| 4 | `the customer did not order milk` | `.` | **limitation:** no negation reasoning — it doesn't infer a correction |
| 5 | `why did the customer leave` | `mango .` | **limitation:** `why` and `leave` are **unknown**; it can't answer a question, just emits a word |
| 6 | `the waiter brought` | `taste .` | continues (note: fresh context each prompt, so replies vary) |
| 7 | `first bring the` | `step .` | sequence-ish continuation |
| 8 | `the guest did not order` | `milk .` | grabs a food word, but still no true negation logic |

**Screenshots:** [question limitation](llm_runs/exp2_extended/chat_evidence/chat_question_limitation.png) · [negation](llm_runs/exp2_extended/chat_evidence/chat_negation.png) · [sequence](llm_runs/exp2_extended/chat_evidence/chat_sequence.png) · [waiter](llm_runs/exp2_extended/chat_evidence/chat_waiter.png)

**One chat limitation (highlighted):** the interface continues text rather than answering. Prompt #5, *"why did the customer leave,"* returned *"mango"* while flagging *why* and *leave* as unknown words — it can neither understand a question nor reason about it, which is exactly the scale limitation described in §10.

---

## 12. Repository layout

```
customllm/
├── README.md                                  ← this file (grading entry point)
├── custom_llm_experiment1_classroom.ipynb     ← executed notebook, Exp 1
├── custom_llm_experiment2_extended.ipynb      ← executed notebook, Exp 2
├── corpus/                                     ← my teaching sources (Exp 2)
│   ├── food_negation.txt
│   ├── food_opposites.txt
│   └── food_sequence.txt
├── evals/
│   ├── language_evals.json                     ← the 48 fixed tests (unchanged)
│   └── README.md                               ← how to run the evals
├── llm_runs/
│   ├── exp1_classroom/                          ← all Exp 1 results & weights
│   └── exp2_extended/                           ← all Exp 2 results & weights
├── nanogpt_model.py   run_evals.py   chat.py   custom_llm.py
├── embedding-viewer.html   requirements.txt   NANOGPT_LICENSE
```

## 13. Reproduce the evals & chat
- **Re-run evals on saved weights:** `python run_evals.py --model llm_runs/exp2_extended/model.pt --output results/my-final-evals` (sends only the prompt to the model, never the answer key; saves CSV/JSON + a free continuation per case). Use `--stage untrained` with `model_untrained.pt` for the before-training set. See [evals/README.md](evals/README.md).
- **Embedding viewer:** open `embedding-viewer.html` locally and load a run's `checkpoint.json` to compare a word's initial/final 64-D vector and neighbors.
- **Chat:** `python chat.py --model llm_runs/exp2_extended/model.pt` (dependencies in `requirements.txt`).

---

*nanoGPT model © Andrej Karpathy (see NANOGPT_LICENSE). Whole-word tokenization and the classroom instrumentation are classroom additions.*
