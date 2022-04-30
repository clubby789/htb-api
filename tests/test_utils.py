from pytest import raises
from datetime import timedelta

from hackthebox.utils import parse_delta


def test_parse_delta():
    assert parse_delta("10s") == timedelta(seconds=10)
    assert parse_delta("10m 10s") == timedelta(minutes=10, seconds=10)
    assert parse_delta("10h 10m 10s") == timedelta(hours=10, minutes=10, seconds=10)
    assert parse_delta("10D 10h 10m 10s") == timedelta(
        days=10, hours=10, minutes=10, seconds=10
    )
    assert parse_delta("10W 10D 10h") == timedelta(weeks=10, days=10, hours=10)
    assert parse_delta("10W 10D 10h 10m 10s") == timedelta(
        weeks=10, days=10, hours=10, minutes=10, seconds=10
    )
    assert parse_delta("10Y 10M 10D") == timedelta(days=(10 * 365) + (10 * 30) + 10)
    with raises(ValueError):
        parse_delta("not a timestamp")
