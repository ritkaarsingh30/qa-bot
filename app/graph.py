"""Single responsibility: assemble nodes and edges into a compiled LangGraph with the SQLite checkpointer."""


def build_graph():
    """Build and compile the graph: classify -> (rewrite -> retrieve -> generate | direct_reply)."""
    # TODO: StateGraph(State), add nodes, entry point, conditional edge, END edges
    # TODO: attach SqliteSaver (SQLITE_PATH) as the checkpointer
    pass
