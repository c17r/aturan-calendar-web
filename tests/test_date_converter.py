from unittest.mock import MagicMock, patch
from datetime import datetime
import pytest

from aturan_calendar_web.converters import DateConverter


def test_to_python_invalid():
    dc = DateConverter(None)
    dt = '10/30/2016'

    with pytest.raises(ValueError):
        rv = dc.to_python(dt)


def test_to_python_valid():
    dc = DateConverter(None)
    dt = '2016-10-30'

    rv = dc.to_python(dt)

    assert rv.year == 2016
    assert rv.month == 10
    assert rv.day == 30


def test_to_url_valid():
    dc = DateConverter(None)
    now = datetime.now()
    expected = now.strftime('%Y-%m-%d')

    actual = dc.to_url(now)

    assert actual == expected
