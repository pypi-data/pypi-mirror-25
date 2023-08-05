# Lie2Me

A python library to validate user input.


## Overview

This library revolves around two main concepts: forms and fields. They can be used to validate
different kinds of user input, like from html forms or a JSON API. Here's an example of a simple form:

```python
from lie2me import Form, fields


class TaskForm(Form):

    title = fields.Text(max=200)
    description = fields.Text(multiline=True, required=False)
    category = fields.Text(options=['feature', 'improvement', 'bug'])
    deadline = fields.DateTime(required=False)
```


## Install

Lie2Me is available in the Python Package Index:

    pip install lie2me


## Forms

A form is a collection of fields. They can be used to express the rules around the desired input
using fields. On top of that, a form can also define it's own validation.

Example:

```python
from lie2me import Form, fields


class SignupForm(Form):

    email = fields.Email()
    password = fields.Password()
    password2 = fields.Password()

    def validate(self, data):
        if 'password' in data and 'password2' in data:
            if data['password'] != data['password2']:
                self.error('password2', 'Password confirmation does not match.')
        return data
```

Note that it's important to check if the fields you're checking are opn the `data` dict, because
form validation will run even if the user did not provide all fields. This happens so the user can
receive the most error messages at once (users can feel anoyed if they correct all errors, only
to get new ones in the next submission).

Using the above form to receive input looks something like this:

```python
valid_data = {'email': 'foo@bar.com', 'password': '123456', 'password2': '123456'}
invalid_data = {'email': 'foobar', 'password': '123456', 'password2': '123'}

form = SignupForm(valid_data)
form.submit()
form.valid # True
form.errors # {}

form = SignupForm(invalid_data)
form.submit()
form.valid # False
form.errors # {'email': 'Invalid email.', 'password2': 'Password confirmation does not match.'}
```

Note how you need to "submit" the form before checking if it's valid and the errors. Before the
submit, form validity will be inconclusive and there will be no errors.

```python
form = SignupForm(invalid_data)
form.valid # None
form.errors # {}
```

Instantiating a form without submitting it can actually be useful when you're presenting the form
to the user for the first time and you don't want to give him errors right away.

```python
form = SignupForm()
form.data # data

form = SignupForm({'email': 'Fill this'})
form.data # {'email': 'Fill this'}
```

After submission, data values can be sanitized and even change types entirely. What happen is,
before submission data is what the form received at the constructor. After as successful submission
`form.data` will contain the sanitized data. Data will be unchanged if the validation reveals
errors.


## Nested Forms

Forms can be nested. This means the validation happens recursively and errors will be nested in the
same structure as the forms. Example:

```python
from lie2me import Form, fields


class AddressForm(Form):

    street = fields.Text(max=200)
    number = fields.Integer(min=0)
    complement = fields.Text(required=False)


class SignupForm(Form):

    email = fields.Email()
    password = fields.Password(min=8)
    address = AddressForm


invalid_data = {'email': 'foo@bar.com', 'password': '123'}
form = SignupForm(invalid_data)
form.submit()
form.errors == {
    'password': 'Must be at least 8 characters long.',
    'address': {
        'street': 'This is required.',
        'number': 'This is required.',
    }
}
```


## Fields

Fields are the core objects to define your validation scheme. There are a lot of builtin fields to
use out of the box, here's examples of them:

```python
from lie2me import fields

fields.Boolean()
fields.Boolean(default=False)

fields.Integer()
fields.Integer(min=1, max=10)

fields.Decimal()
fields.Decimal(min=1.50, max=3.50)

fields.Float()
fields.Float(min=1.50, max=3.50)

fields.Text()
fields.Text(min=3, max=144)
fields.Text(options=['feature', 'improvement', 'bug'])

fields.Email()
fields.Email(required=False)

fields.Password()
fields.Password(min=8, max=1024)

fields.Date()
fields.Date(min='1990-01-01', max='2017-12-31')

fields.Time()
fields.Time(timezone=False)
fields.Time(timezone=True)
fields.Time(min='08:00', max='18:00')

fields.DateTime()
fields.DateTime(timezone=False)
fields.DateTime(timezone=True)
fields.DateTime(min='2017-09-22 08:00+00:00', max='2017-09-22 18:00+00:00')

fields.List(fields.Integer(min=1, max=5))
fields.List(AddressForm)
```

All fields have the `required` and `default` configurations. They also support messages that can
be overriden by the `messages` configuration:

```python
fields.Integer(min=1, max=5, messages={
    'min': 'No less than 1 star.',
    'max': 'No more than {max} stars.'
})
```
