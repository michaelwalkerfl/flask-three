from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import PasswordField
from wtforms import SubmitField

from wtforms.validators import DataRequired
from wtforms.validators import Email
from wtforms.validators import EqualTo
from wtforms.validators import Length


class UserRegistrationForm(FlaskForm):
    """User Registration Form."""
    first_name = StringField(
        'First Name',
        validators=[DataRequired()],
    )
    last_name = StringField(
        'Last Name',
        validators=[DataRequired()],
    )
    email = StringField(
        'Email Address',
        validators=[
            Length(min=6),
            Email(message='Enter a valid email address.'),
            DataRequired(),
        ],
    )
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(),
            Length(
                min=8,
                message='You need to enter a stronger password.',
            ),
        ],
    )
    password_confirm = PasswordField(
        'Confirm Password',
        validators=[
            DataRequired(),
            EqualTo('password', message='Passwords must match.'),
        ],
    )
    submit = SubmitField('Register')


class UserLoginForm(FlaskForm):
    """User Log-in Form."""
    email = StringField(
        'Email',
        validators=[
            DataRequired(),
            Email(message='Enter a valid email address.'),
        ],
    )
    password = PasswordField(
        'Password',
        validators=[DataRequired()],
    )
    submit = SubmitField('Log-in')
