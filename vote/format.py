"""Helpers for formatting dates and amounts for display."""

import datetime
from decimal import ROUND_HALF_UP, Decimal


def format_date(d: datetime.date) -> str:
    """Return the date as an ISO 8601 YYYY-MM-DD string."""
    return d.isoformat()[:10]


def format_amount(n: float) -> str:
    """Format a number with two decimals, rounding half up."""
    return str(
        Decimal(str(n)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    )
