import datetime

import pytest

import isaric.pydantic_types as T


def test_integer_range():
    r = T.IntegerRange(start=4, end=5)
    assert (r.start, r.end) == (4, 5)
    with pytest.raises(ValueError):
        T.IntegerRange(start=5, end=2)


def test_date_range():
    next_weekday = (datetime.datetime.today() + datetime.timedelta(days=7)).date()
    today = datetime.datetime.today().date()
    r = T.DateRange(start="2022-01-01", end="2022-05-01")
    assert (r.start, r.end) == (datetime.date(2022, 1, 1), datetime.date(2022, 5, 1))

    # Disallow future dates
    with pytest.raises(ValueError):
        T.DateRange(start=today, end=next_weekday)

    # Start date is after end date
    with pytest.raises(ValueError):
        T.DateRange(start="2022-05-01", end="2022-01-01")
