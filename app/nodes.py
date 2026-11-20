"""Single responsibility: the graph's node functions. Each reads State and returns a partial State update."""

from app.state import State


def classify(state: State) -> dict:
    """Decide whether the latest user message is a docs question or off-topic."""
    # TODO: LLM call with a strict prompt; return {"route": "docs" | "other"}
    pass


def route_after_classify(state: State) -> str:
    """Conditional-edge function: return the name of the next node based on state['route']."""
    # TODO: return "rewrite" or "direct_reply"
    pass


def rewrite(state: State) -> dict:
    """Turn the latest message plus history into a standalone search query."""
    # TODO: LLM call using recent messages; return {"rewritten_query": ...}
    pass


def retrieve(state: State) -> dict:
    """Search Chroma with the rewritten query."""
    # TODO: call vectorstore.search; return {"retrieved_docs": ...}
    pass


def generate(state: State) -> dict:
    """Answer using only the retrieved chunks, citing sources."""
    # TODO: LLM call grounded in retrieved_docs; return answer, sources, and the new assistant message
    pass


def direct_reply(state: State) -> dict:
    """Short reply for off-topic or chit-chat input."""
    # TODO: return answer and the new assistant message
    pass
