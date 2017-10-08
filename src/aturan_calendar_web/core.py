import os
import calendar

from flask import Flask, json, render_template
from . import converters

from docutils.core import publish_parts
import jinja2
import arrow
import aturan_calendar as cal

CURRENT_PATH = os.path.dirname(__file__)

app = Flask(__name__)
app.url_map.converters['date'] = converters.DateConverter


def week_of_month(date):
    rv = None
    date = arrow.get(date)
    calendar.setfirstweekday(calendar.SUNDAY)
    weeks = calendar.monthcalendar(date.year, date.month)
    for week, days in enumerate(weeks):
        days = [d for d in days if d > 0]
        if date.day in days:
            rv = week + 1
            break
    return rv


@app.route('/')
def homepage():
    now = arrow.utcnow()
    aturan = cal.western_to_aturan(now)
    return render_template(
        'home.html',
        today={
            'day_of_year': now.format('DDD'),
            'day_of_week': now.format('dddd'),
            'month_of_year': now.format('MMMM'),
            'week_of_month': week_of_month(now),
            'year': now.year,
            'month': now.month,
            'day': now.day,
        },
        aturan=aturan,
        text=cal.__doc__
    )


@app.route('/date/<date:date>')
def api_date(date):
    return json.jsonify(cal.western_to_aturan(date))


@app.route('/year/<int:year>')
def api_year(year):
    return json.jsonify(cal.aturan_calendar_for_western_year(year))


@app.template_filter('ordinal')
def ordinal(num):
    try:
        num = int(num)
    except ValueError:
        return num

    exceptions = {
        11: "{}th",
        12: "{}th",
        13: "{}th",

        1: "{}st",
        2: "{}nd",
        3: "{}rd",
    }
    fmt = exceptions.get((num % 100), None)
    if not fmt:
        fmt = exceptions.get((num % 10), None)
    if not fmt:
        fmt = "{}th"

    return fmt.format(num)


@app.template_filter('version')
def version(filename):
    fullpath = os.path.join(CURRENT_PATH, filename[1:])
    try:
        timestamp = str(os.path.getmtime(fullpath))
    except OSError:
        return filename
    return "{0}?v={1}".format(filename, timestamp)


@app.template_filter('rst')
def rst(text):
    return jinja2.Markup(publish_parts(source=text, writer_name='html')['body'])
