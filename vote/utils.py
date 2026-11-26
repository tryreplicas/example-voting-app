def normalize_option(option):
    """Normalize option by trimming whitespace and lowercasing."""
    return option.strip().lower()


def is_valid_vote(vote):
    """Check if vote is a non-empty string after stripping whitespace."""
    return isinstance(vote, str) and len(vote.strip()) > 0


def sorted_tally(tally):
    """Return tally dict sorted by keys."""
    return {k: v for k, v in sorted(tally.items())}
