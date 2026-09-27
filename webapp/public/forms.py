from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, Length


class ContactForm(FlaskForm):
    """Public contact form."""

    name = StringField('Name', validators=[DataRequired(), Length(max=100)])
    email = StringField(
        'Email Address',
        validators=[DataRequired(), Email(message='Enter a valid email address.')],
    )
    subject = StringField('Subject', validators=[DataRequired(), Length(max=150)])
    message = TextAreaField('Message', validators=[DataRequired(), Length(min=10, max=5000)])
    submit = SubmitField('Send message')
