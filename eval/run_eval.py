"""Single responsibility: run every case in cases.json through the graph, score it, and print a summary."""

# Case shape (see cases.json):
#   question, history (optional), expected_source, reference_answer, should_route_to


def load_cases(path: str) -> list[dict]:
    """Read the eval cases from JSON."""
    # TODO
    pass


def run_case(case: dict) -> dict:
    """Run one case through the graph (fresh thread_id); return route, retrieved sources, answer."""
    # TODO: invoke graph directly, no HTTP
    pass


def score_routing(case: dict, result: dict) -> bool:
    """Free check: did the route match should_route_to?"""
    # TODO
    pass


def score_retrieval(case: dict, result: dict) -> bool:
    """Free check: did expected_source appear among the retrieved sources?"""
    # TODO
    pass


def main() -> None:
    """Run all cases, print per-case results and overall percentages."""
    # TODO: add throttling between calls for free-tier rate limits
    # TODO: later, call eval.judge for correctness and faithfulness
    pass


if __name__ == "__main__":
    main()
