from datetime import datetime
from werkzeug.routing import BaseConverter, ValidationError


class DateConverter(BaseConverter):
    """Extracts a ISO8601 date from path and validates it"""

    regex = r'\d{4}-\d{2}-\d{2}'

    def to_python(self, value):
        try:
            return datetime.strptime(value, '%Y-%m-%d').date()
        except ValueError:
            raise ValidationError('Must be YYYY-MM-DD format')

    def to_url(self, value):
        return value.strftime('%Y-%m-%d')
