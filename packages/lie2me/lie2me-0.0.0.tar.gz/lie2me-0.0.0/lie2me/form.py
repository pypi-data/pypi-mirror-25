from .field import Field
from .exceptions import FieldValidationError, BadFormValidationError


class Form(object):

    def __init__(self, data=None):
        self.fields, self.forms = self._get_fields_and_nested_forms()
        self._initialize_data(data)
        self.errors = {}
        self.valid = None

    def _get_fields_and_nested_forms(self):
        fields = {}
        forms = {}
        for key in dir(self):
            if not key.startswith('_'):
                attr = getattr(self, key)
                if isinstance(attr, Field):
                    fields[key] = attr
                if isinstance(attr, type) and issubclass(attr, Form):
                    forms[key] = attr
        return fields, forms

    def _initialize_data(self, data):
        data = data if hasattr(data, 'get') else None
        self.data = data or {}
        if data is None:
            for key, form in self.forms.items():
                self.data[key] = {}

    def submit(self):
        data = {}
        data.update(self._validate_fields())
        data.update(self._validate_forms())
        data = self.validate(data)
        self.valid = not self.errors
        if self.valid:
            if data is None:
                raise BadFormValidationError()
            self.data = data

    def _validate_fields(self):
        data = {}
        for key, field in self.fields.items():
            try:
                value = field.submit(self.data.get(key))
                data[key] = value
            except FieldValidationError as e:
                self.errors[key] = e.data
        return data

    def _validate_forms(self):
        data = {}
        for key, form in self.forms.items():
            f = form(self.data.get(key))
            f.submit()
            if f.valid:
                data[key] = f.data
            else:
                self.errors[key] = f.errors
        return data

    def validate(self, data):
        return data

    def error(self, key, message):
        self.errors[key] = message
