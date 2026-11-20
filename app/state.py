"""Single responsibility: define the shape of the graph State."""

# from typing import TypedDict


class State:  # TODO: make this a TypedDict
    """Shared data passed between graph nodes and saved by the checkpointer."""

    # TODO: fields
    #   messages         - conversation history; must APPEND across turns (use a reducer)
    #   route            - "docs" or "other" (set by classify)
    #   rewritten_query  - standalone search query (set by rewrite)
    #   retrieved_docs   - chunks from retrieve (replaced each turn)
    #   answer           - final text (set by generate / direct_reply)
    #   sources          - list of source files cited
    #   retry_count      - reserved for Option C
    pass
