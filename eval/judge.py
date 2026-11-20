"""Single responsibility: LLM-as-judge scoring (Groq). Stage 3 of the eval plan."""


def judge_correctness(question: str, reference: str, answer: str) -> dict:
    """Does the answer convey the same facts as the reference? Return {"pass": bool, "reason": str}."""
    # TODO: strict prompt + structured output
    pass


def judge_faithfulness(answer: str, chunks: list[str]) -> dict:
    """Is every claim in the answer supported by the chunks? Return {"pass": bool, "reason": str}."""
    # TODO: strict prompt + structured output
    pass
