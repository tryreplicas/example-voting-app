from vote.tally import count_votes, get_leading_option


def test_count_votes_empty_list():
    """Test count_votes with an empty list."""
    assert count_votes([]) == {}
