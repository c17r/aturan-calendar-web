import calendar

from flask import Flask, json, render_template
import converters

import arrow
import aturan_calendar as cal


app = Flask(__name__)
app.url_map.converters['date'] = converters.DateConverter


def week_of_month(date):
    weeks = calendar.monthcalendar(date.year, date.month)
    week = 0
    for days in weeks:
        week += 1
        begin = days[0]
        end = days[-1]
        if (begin == 0 or date.day >= begin) and (date.day <= end or end == 0):
            return week


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
    return json.dumps(cal.western_to_aturan(date))


@app.route('/year/<int:year>')
def api_year(year):
    return json.dumps(cal.aturan_calendar_for_western_year(year))


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


if __name__ == '__main__':
    app.config['DEBUG'] = True
    app.config['PROPAGATE_EXCEPTIONS'] = True
    app.run()
