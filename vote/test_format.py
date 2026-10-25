import datetime

from format import format_amount, format_date, format_percent


def test_format_date():
    assert format_date(datetime.date(2026, 10, 25)) == "2026-10-25"


def test_format_amount():
    assert format_amount(3) == "3.00"
    assert format_amount(2.675) == "2.68"


def test_format_percent():
    assert format_percent(12.5) == "12.5%"
    assert format_percent(0) == "0.0%"
    assert format_percent(12.25) == "12.3%"
