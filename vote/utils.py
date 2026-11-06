def normalize_option(option):
    return option.strip().lower()


def is_valid_vote(vote):
    return isinstance(vote, str) and len(vote) > 0


def format_tally(tally):
    return {k: v for k, v in sorted(tally.items())}
