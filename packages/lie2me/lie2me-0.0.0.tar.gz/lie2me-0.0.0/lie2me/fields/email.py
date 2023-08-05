import re
from ..field import Field


class Email(Field):

    messages = {
        'type': 'Invalid email.',
    }

    def validate(self, value):
        value = super(Email, self).validate(value)
        if len(value) > 254:
            raise self.error('type')
        if not re.match(r'^[^@]+@[^@]+\.[^@]+$', value):
            raise self.error('type')
        return value
