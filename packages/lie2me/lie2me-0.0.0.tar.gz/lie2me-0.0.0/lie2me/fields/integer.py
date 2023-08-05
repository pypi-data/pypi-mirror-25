from ..field import Field


class Integer(Field):

    min = None
    max = None

    messages = {
        'type': 'Invalid number.',
        'min': 'Must not be lower than {min}.',
        'max': 'Must not be higher than {max}.',
    }

    def validate(self, value):
        value = super(Integer, self).validate(value)
        try:
            value = int(value)
        except:
            raise self.error('type')
        if self.min is not None and value < self.min:
            raise self.error('min')
        if self.max is not None and value > self.max:
            raise self.error('max')
        return value
