"""Single responsibility: hold all settings (paths, model names, chunk size, k) in one place."""

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# --- Stage 1: chunking ---
DOCS_DIR = ROOT / "data" / "docs"
CHUNKS_PATH = ROOT / "data" / "chunks.jsonl"
DOCS_SITE = "https://docs.langchain.com"
DOCS_URL_PREFIX = "/oss/python/langgraph"  # used to build each page's citation URL
MAX_CHUNK_TOKENS = 800  # rough estimate (chars / 4). Lower to ~200 if you switch to MiniLM, then regenerate.

# TODO: load .env (python-dotenv)
# TODO: define constants: CHROMA_DIR, SQLITE_PATH, COLLECTION_NAME,
#       EMBEDDING_MODEL, LLM_MODEL, JUDGE_MODEL, TOP_K
