"""Helpers for formatting dates and amounts for display."""

import datetime
from decimal import ROUND_HALF_UP, Decimal


def format_date(d: datetime.date) -> str:
    """Return the date as an ISO 8601 YYYY-MM-DD string.

    Example: 2026-10-25.
    """
    return d.isoformat()[:10]


def format_amount(amount: float) -> str:
    """Return amount as a string with two decimal places, rounding half up."""
    return str(
        Decimal(str(amount)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    )


def format_percent(x: float) -> str:
    """Return x as a percentage string with one decimal place, rounding half up.

    Example: 12.5 becomes "12.5%".
    """
    return (
        str(Decimal(str(x)).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP))
        + "%"
    )
