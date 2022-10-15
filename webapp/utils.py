import os

from flask import url_for
from wtforms.fields import Field
from wtforms.widgets import HiddenInput


def parse_env():
    if os.path.exists('config.env'):
        for line in open('config.env'):
            env_var = line.strip().split('=')
            if len(env_var) == 2:
                os.environ[env_var[0]] = env_var[1].replace('\"', '')


def register_template_utils(app):
    """Register Jinja2 helpers."""

    @app.template_test()
    def equal_to(value, other):
        return value == other

    @app.template_global()
    def is_hidden_field(field):
        from wtforms.fields import HiddenField
        return isinstance(field, HiddenField)

    app.add_template_global(role_specific_index)


def role_specific_index(role):
    return url_for(role.index)


class CustomSelectField(Field):
    widget = HiddenInput()

    def __init__(self, label='', validators=None, multiple=False,
                 choices=None, allow_custom=True, **kwargs):
        super(CustomSelectField, self).__init__(label, validators,
                                                **kwargs)
        self.data = None
        if choices is None:
            choices = []
        self.multiple = multiple
        self.choices = choices
        self.allow_custom = allow_custom

    def _value(self):
        return self.data if self.data is not None else ''

    def process_form_data(self, value_list):
        if value_list:
            self.data = value_list[1]
            self.raw_data = [value_list[1]]
        else:
            self.data = ''
