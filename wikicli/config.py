"""All paths and tunable settings in one place."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Obsidian vault (open vault/ itself in Obsidian)
VAULT = ROOT / "vault"
RAW_DIR = VAULT / "raw"            # original sources, never modified
WIKI_DIR = VAULT / "wiki"          # generated + reviewed notes
INDEX_FILE = VAULT / "index.md"    # human landing page

# Machine files live OUTSIDE the vault
DATA_DIR = ROOT / "data"
CHUNKS_FILE = DATA_DIR / "chunks.json"
CATALOG_FILE = DATA_DIR / "source_catalog.json"

PROMPTS_DIR = ROOT / "prompts"
EVIDENCE_DIR = ROOT / "evidence"

# Model: Gemma 4 E2B instruction-tuned, 4-bit MLX quantization (runs on an 8 GB M1)
MODEL_ID = "mlx-community/gemma-4-e2b-it-4bit"
EXECUTION_MODE = "local"

# Retrieval
PASSAGE_CHARS = 900        # target max size of one passage
TOP_K = 4                  # passages passed to Gemma in ask mode
MIN_SCORE = 2.0            # below this top BM25 score we treat retrieval as "nothing relevant"

# Generation
ASK_MAX_TOKENS = 350
CHAT_MAX_TOKENS = 400
INGEST_MAX_TOKENS = 700
INGEST_INPUT_CHARS = 6000  # max characters of a source sent to Gemma in one ingest call
CHAT_HISTORY_TURNS = 6     # user+assistant messages kept in chat context
