"""Single responsibility: one-off pipeline from raw Markdown docs to a populated Chroma index."""


def load_docs(docs_dir: str) -> list[dict]:
    """Read every .md file; return a list of {text, source}."""
    # TODO: walk docs_dir, read files, keep relative path as source
    pass


def chunk_docs(docs: list[dict]) -> list[dict]:
    """Split documents into chunks, keeping source metadata on each chunk."""
    # TODO: Markdown-aware splitter using CHUNK_SIZE / CHUNK_OVERLAP
    pass


def build_index() -> None:
    """Run load -> chunk -> store. Entry point for `python -m app.ingest`."""
    # TODO: wire the steps; rebuild the collection from scratch
    pass


if __name__ == "__main__":
    build_index()
