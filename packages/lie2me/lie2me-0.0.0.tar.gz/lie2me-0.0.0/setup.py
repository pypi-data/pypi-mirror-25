from setuptools import setup

long_description = """
This library uses forms and fields to define validation rules in a declarative manner. They can be
then used to validate user input and provide sanitized data.
"""

setup(
    name = 'lie2me',
    version = '0.0.0',

    packages = ['lie2me', 'lie2me.fields'],
    include_package_data = True,

    install_requires = [],
    entry_points = {'console_scripts': []},

    author = 'Hugo Leonardo Leão Mota',
    author_email = 'hugo.txt@gmail.com',
    license = 'MIT',
    url = 'https://github.com/hugollm/lie2me',

    keywords = 'form fields validation user input',
    description = 'A python library to validate user input.',

    long_description = long_description,
)
