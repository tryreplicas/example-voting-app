import datetime

from format import (
    format_amount,
    format_bytes,
    format_date,
    format_percent,
    format_ratio,
)


def test_format_date():
    assert format_date(datetime.date(2026, 10, 25)) == "2026-10-25"


def test_format_amount():
    assert format_amount(3) == "3.00"
    assert format_amount(2.675) == "2.68"


def test_format_percent():
    assert format_percent(12.5) == "12.5%"
    assert format_percent(0) == "0.0%"
    assert format_percent(12.25) == "12.3%"


def test_format_ratio():
    assert format_ratio(4, 6) == "2:3"
    assert format_ratio(5, 7) == "5:7"
    assert format_ratio(3, 3) == "1:1"
    assert format_ratio(0, 5) == "0:1"
    assert format_ratio(0, 0) == "0:0"


def test_format_bytes():
    assert format_bytes(0) == "0.0 B"
    assert format_bytes(512) == "512.0 B"
    assert format_bytes(1536) == "1.5 KB"
    assert format_bytes(1048576) == "1.0 MB"
    assert format_bytes(1024**3) == "1.0 GB"
    assert format_bytes(1024**4) == "1.0 TB"
