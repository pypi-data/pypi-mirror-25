import re
from . import exceptions


class Field(object):

    required = True
    default = None

    messages = {
        'required': 'This is required.',
    }

    def __init__(self, *args, **kwargs):
        if args:
            raise exceptions.PositionalArgumentFieldError()
        self.messages = self._assemble_class_messages()
        self._update_attributes(kwargs)

    def _assemble_class_messages(self):
        messages = {}
        for cls in reversed(self.__class__.__mro__):
            if hasattr(cls, 'messages'):
                messages.update(cls.messages)
        return messages

    def _update_attributes(self, kwargs):
        for key, value in kwargs.items():
            if not hasattr(self, key):
                raise exceptions.InvalidFieldArgumentError(self.__class__, key)
            if key == 'messages':
                self.messages.update(value)
            else:
                setattr(self, key, value)

    def submit(self, value):
        try:
            return self.validate(value)
        except exceptions.FieldAbortValidation as e:
            return e.value

    def validate(self, value):
        if value is not None:
            value = str(value).strip()
        if not value and self.default is not None:
            value = str(self.default).strip()
        if not value and self.required:
            raise self.error('required')
        if not value:
            raise self.abort(None)
        return value

    def error(self, message):
        message = self.messages.get(message, message)
        message = self.format_message(message)
        return exceptions.FieldValidationError(message)

    def abort(self, value):
        raise exceptions.FieldAbortValidation(value)

    def format_message(self, message):
        matches = re.findall(r'\{([a-zA-Z][a-zA-Z0-9_]*?)\}', message)
        for match in matches:
            placeholder = '{' + match + '}'
            message = message.replace(placeholder, str(getattr(self, match)))
        return message
