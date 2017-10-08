"""
aturan_calendar_web
~~~~~~~~~~~~~~~~~~~
Converts current Gregorian date into the Aturan calendar and shows both dates.

Also provides an API:
    - /date/YYYY-MM-DD: Converts provided date into Aturan
    - /year/YYYY: Returns entire calendar list for provided Aturan year

:copyright: 2016-2017 Christian Erick Sauer.
:license: MIT, see LICENSE for more details.

All rights regarding The Kingkiller Chronicles are reserved by Patrick Rothfuss.

see http://github.com/c17r/aturan-calendar for more information on the date conversion.

"""  # noqa

from .core import *  # noqa
