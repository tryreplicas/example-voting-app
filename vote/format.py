from decimal import ROUND_HALF_UP, Decimal


def format_date(d):
    return d.isoformat()[:10]


def format_amount(n: float) -> str:
    return str(Decimal(str(n)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))
