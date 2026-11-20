"""Single responsibility: turn text into vectors. The only file that knows which embedding model is used."""


def embed_texts(texts: list[str]) -> list[list[float]]:
    """Embed many document chunks (ingestion)."""
    # TODO: call Gemini embeddings; handle rate limits (batching / retry)
    pass


def embed_query(text: str) -> list[float]:
    """Embed one user query (retrieval)."""
    # TODO: same model as embed_texts; swapping to local MiniLM happens only here
    pass
