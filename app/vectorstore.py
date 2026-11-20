"""Single responsibility: read and write the Chroma collection. Nothing else touches Chroma."""


def get_collection():
    """Open (or create) the persistent Chroma collection."""
    # TODO: PersistentClient at CHROMA_DIR, get_or_create_collection
    pass


def add_chunks(chunks: list[dict]) -> None:
    """Store chunks (text + metadata such as source file) with their embeddings."""
    # TODO: embed texts, upsert with ids and metadata
    pass


def search(query: str, k: int) -> list[dict]:
    """Return the top-k chunks for a query, each with text and source metadata."""
    # TODO: embed query, query collection, reshape results into a list of dicts
    pass
