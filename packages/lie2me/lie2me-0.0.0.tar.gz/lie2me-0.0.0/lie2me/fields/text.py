import re
from ..field import Field


class Text(Field):

    min = None
    max = None
    multiline = False
    pattern = None
    options = None
    trim = True

    messages = {
        'min': 'Must be at least {min} characters long.',
        'max': 'Must have no more than {max} characters.',
        'multiline': 'Must not have more than one line.',
        'pattern': 'Invalid format.',
        'options': 'Invalid option.',
    }

    def validate(self, value):
        if value is not None:
            value = str(value)
            if self.trim:
                value = value.strip()
        if not value and self.default is not None:
            value = str(self.default)
            if self.trim:
                value = value.strip()
        if not value and self.required:
            raise self.error('required')
        if not value:
            raise self.abort(None)
        if self.min is not None and len(value) < self.min:
            raise self.error('min')
        if self.max is not None and len(value) > self.max:
            raise self.error('max')
        if not self.multiline and len(value.splitlines()) > 1:
            raise self.error('multiline')
        if self.pattern and not re.match(self.pattern, value, flags=re.MULTILINE|re.DOTALL):
            raise self.error('pattern')
        if self.options and value not in self.options:
            raise self.error('options')
        return value
