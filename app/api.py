"""Single responsibility: HTTP layer. Receive requests, call the graph with conversation_id as thread_id, return the result."""


class ChatRequest:  # TODO: make this a pydantic BaseModel
    """Incoming body: message (required), conversation_id (optional)."""

    pass


class ChatResponse:  # TODO: make this a pydantic BaseModel
    """Outgoing body: conversation_id, answer, sources."""

    pass


def chat(request: ChatRequest) -> ChatResponse:
    """POST /chat handler."""
    # TODO: generate conversation_id if missing
    # TODO: invoke graph with config {"configurable": {"thread_id": conversation_id}}
    # TODO: return answer, sources, conversation_id
    pass


def health() -> dict:
    """GET /health handler."""
    # TODO: return a simple status
    pass


# TODO: create the FastAPI app, build the graph once at startup, register the routes
