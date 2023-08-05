from decimal import Decimal as D
from ..field import Field


class Decimal(Field):

    min = None
    max = None

    messages = {
        'type': 'Invalid number.',
        'min': 'Must not be lower than {min}.',
        'max': 'Must not be higher than {max}.',
    }

    def validate(self, value):
        value = super(Decimal, self).validate(value)
        try:
            value = D(value)
        except:
            raise self.error('type')
        if self.min is not None and value < D(str(self.min)):
            raise self.error('min')
        if self.max is not None and value > D(str(self.max)):
            raise self.error('max')
        return value
