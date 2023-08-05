from ..field import Field


class Password(Field):

    min = None
    max = None

    messages = {
        'min': 'Must be at least {min} characters long.',
        'max': 'Must have no more than {max} characters.',
    }

    def validate(self, value):
        if value is not None:
            value = str(value)
        if not value and self.default is not None:
            value = str(self.default)
        if not value and self.required:
            raise self.error('required')
        if not value:
            raise self.abort(None)
        if self.min is not None and len(value) < self.min:
            raise self.error('min')
        if self.max is not None and len(value) > self.max:
            raise self.error('max')
        return value
