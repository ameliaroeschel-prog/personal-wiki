# Ingest attempt 1 (kept as evidence)

Run: `./wiki ingest vault/raw`, 2026-09-27, local Gemma 4 E2B 4-bit, ~45 s total (11–15 s per source, peak 4.3 GB).

**Failure found in review:** the prompt told Gemma to "prefer reusing a name from the existing
concept list". After the first source created Corpus / Evaluation Suite / Learning Rate / Loss,
Gemma attached all four to the next sources even when they did not fit:

- `Card Catalog Tracker` → `[[Learning Rate]]` "This concept is not explicitly mentioned in the source document."
- `Card Catalog Tracker` → `[[Evaluation Suite]]` described as database connectivity (wrong).
- `PacMan DQN Agent` → `[[Corpus]]` "The game pixels are used as the input data" (misleading).

These are meaningless graph links. Fix in attempt 2: (1) prompt says only list concepts the
source actually discusses and that new names are fine; (2) the harness drops any concept whose
usage line says it is not mentioned / not discussed / implied.
