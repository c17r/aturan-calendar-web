from unittest.mock import MagicMock, patch

from aturan_calendar_web.core import version


@patch('aturan_calendar_web.core.os.path.getmtime')
def test_version_invalid(m_mtime):
    filename = '/does/not/exist'
    m_mtime.side_effect = OSError()

    rv = version(filename)

    assert rv == filename


@patch('aturan_calendar_web.core.os.path.getmtime')
def test_version_valid(m_mtime):
    filename = 'lol/what'
    m_mtime.return_value = 'timestamp'

    rv = version(filename)

    assert rv == 'lol/what?v=timestamp'
