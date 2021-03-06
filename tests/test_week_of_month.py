from unittest.mock import MagicMock, patch

from aturan_calendar_web.core import week_of_month


@patch('aturan_calendar_web.core.calendar.monthcalendar')
def test_week_of_month_none(m_cal):
    m_cal.return_value = []

    assert week_of_month('2017-01-01') is None
    m_cal.assert_called_with(2017, 1)


def test_week_of_month_good():
    values = [
        ("2017-10-01", 1), ("2017-10-02", 1), ("2017-10-03", 1), ("2017-10-04", 1), ("2017-10-05", 1),
        ("2017-10-06", 1), ("2017-10-07", 1), ("2017-10-08", 2), ("2017-10-09", 2), ("2017-10-10", 2),
        ("2017-10-11", 2), ("2017-10-12", 2), ("2017-10-13", 2), ("2017-10-14", 2), ("2017-10-15", 3),
        ("2017-10-16", 3), ("2017-10-17", 3), ("2017-10-18", 3), ("2017-10-19", 3), ("2017-10-20", 3),
        ("2017-10-21", 3), ("2017-10-22", 4), ("2017-10-23", 4), ("2017-10-24", 4), ("2017-10-25", 4),
        ("2017-10-26", 4), ("2017-10-27", 4), ("2017-10-28", 4), ("2017-10-29", 5), ("2017-10-30", 5),
        ("2017-10-31", 5),
    ]

    for i, expected in values:
        actual = week_of_month(i)
        assert expected == actual, 'Date {i}: expected: {expected}, got: {actual}'.format(**locals())
