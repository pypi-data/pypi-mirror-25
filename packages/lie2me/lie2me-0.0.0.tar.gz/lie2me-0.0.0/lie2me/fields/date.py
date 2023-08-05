from datetime import datetime

from ..field import Field
from ..parsers import parse_date


class Date(Field):

    format = None
    min = None
    max = None

    messages = {
        'type': 'Invalid date.',
        'min': 'Must not come before {min}.',
        'max': 'Must not come after {max}.',
    }

    def __init__(self, *args, **kwargs):
        super(Date, self).__init__(*args, **kwargs)
        self.parsed_min = self.parse(self.min) if self.min else None
        self.parsed_max = self.parse(self.max) if self.max else None
        if self.min and self.parsed_min is None:
            raise ValueError('Invalid min date.')
        if self.max and self.parsed_max is None:
            raise ValueError('Invalid max date.')

    def validate(self, value):
        value = super(Date, self).validate(value)
        value = self.parse(value)
        if value is None:
            raise self.error('type')
        if self.min and value < self.parsed_min:
            raise self.error('min')
        if self.max and value > self.parsed_max:
            raise self.error('max')
        return value

    def parse(self, value):
        if self.format is None:
            return parse_date(value)
        try:
            return datetime.strptime(value, self.format).date()
        except:
            return None
