class FieldValidationError(Exception):

    def __init__(self, data):
        self.data = data


class FieldAbortValidation(Exception):

    def __init__(self, value):
        self.value = value


class PositionalArgumentFieldError(Exception):

    def __init__(self):
        message = 'Positional arguments are not allowed in fields. Use kwargs.'
        super(PositionalArgumentFieldError, self).__init__(message)


class InvalidFieldArgumentError(Exception):

    def __init__(self, field_type, argument_name):
        message = 'Invalid argument ({}) for field: {}'.format(argument_name, field_type.__name__)
        super(InvalidFieldArgumentError, self).__init__(message)


class BadFormValidationError(Exception):

    def __init__(self):
        message = 'Form validation did not return any data. Did you forget to return?'
        super(BadFormValidationError, self).__init__(message)


class InvalidListTypeError(Exception):

    def __init__(self):
        message = 'List field needs type argument to be a form class or a field instance'
        super(InvalidListTypeError, self).__init__(message)
