"""Single responsibility: construct the chat LLM clients. The only file that knows which providers are used."""


def get_llm():
    """Return the main chat model (Gemini Flash) used by the graph nodes."""
    # TODO: build the Gemini chat model from config
    pass


def get_judge_llm():
    """Return the eval judge model (Groq, largest available model)."""
    # TODO: build the Groq chat model from config
    pass
