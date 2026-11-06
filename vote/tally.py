def count_votes(votes):
    """Count votes from a list into a dict."""
    tally = {}
    for vote in votes:
        tally[vote] = tally.get(vote, 0) + 1
    return tally


def get_leading_option(tally):
    """Return the leading option or None if tally is empty."""
    if not tally:
        return None
    return max(tally, key=tally.get)
