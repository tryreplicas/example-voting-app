from decimal import ROUND_HALF_UP, Decimal


def format_date(d):
    """Return the date as an ISO YYYY-MM-DD string."""
    return d.isoformat()[:10]


def format_amount(n: float) -> str:
    """Format a number with two decimals, rounding half up."""
    return str(Decimal(str(n)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))
