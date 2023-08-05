from ..field import Field
from ..parsers import parse_time


class Time(Field):

    timezone = None
    min = None
    max = None

    messages = {
        'type': 'Invalid time.',
        'naive': 'Requires timezone information.',
        'aware': 'Must not have timezone information.',
        'min': 'Must not come before {min}.',
        'max': 'Must not come after {max}.',
    }

    def __init__(self, *args, **kwargs):
        super(Time, self).__init__(*args, **kwargs)
        self.parsed_min = parse_time(self.min) if self.min else None
        self.parsed_max = parse_time(self.max) if self.max else None
        if self.min and self.parsed_min is None:
            raise ValueError('Invalid min time.')
        if self.max and self.parsed_max is None:
            raise ValueError('Invalid max time.')

    def validate(self, value):
        value = super(Time, self).validate(value)
        value = parse_time(value)
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
