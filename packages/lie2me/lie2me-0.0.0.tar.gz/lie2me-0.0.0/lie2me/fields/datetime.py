from ..field import Field
from ..parsers import parse_datetime


class DateTime(Field):

    timezone = None
    min = None
    max = None

    messages = {
        'type': 'Invalid date or time.',
        'naive': 'Requires timezone information.',
        'aware': 'Must not have timezone information.',
        'min': 'Must not come before {min}.',
        'max': 'Must not come after {max}.',
    }

    def __init__(self, *args, **kwargs):
        super(DateTime, self).__init__(*args, **kwargs)
        self.parsed_min = parse_datetime(self.min) if self.min else None
        self.parsed_max = parse_datetime(self.max) if self.max else None
        if self.min and self.parsed_min is None:
            raise ValueError('Invalid min datetime.')
        if self.max and self.parsed_max is None:
            raise ValueError('Invalid max datetime.')

    def validate(self, value):
        value = super(DateTime, self).validate(value)
        value = parse_datetime(value)
        if value is None:
            raise self.error('type')
        if self.timezone is True and not value.tzinfo:
            raise self.error('naive')
        if self.timezone is False and value.tzinfo:
            raise self.error('aware')
        if self.min and value < self.parsed_min:
            raise self.error('min')
        if self.max and value > self.parsed_max:
            raise self.error('max')
        return value
