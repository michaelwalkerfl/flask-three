from flask import Blueprint, current_app, flash, redirect, render_template, url_for

from webapp.public.forms import ContactForm
from webapp.utils import queue_email

public = Blueprint(
    'public',
    __name__,
    template_folder='templates',
    static_folder='static',
)


@public.route('/', methods=['GET'])
def index():
    return render_template('index.jinja2')


@public.route('/about', methods=['GET'])
def about():
    return render_template('about.jinja2')


@public.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        recipient = current_app.config.get('ADMIN_EMAIL')
        body = f'From: {form.name.data} <{form.email.data}>\n\n{form.message.data}'
        if recipient and queue_email(f'Contact form: {form.subject.data}', body, recipient):
            flash('Thanks for reaching out. We will get back to you soon.', 'success')
            return redirect(url_for('public.contact'))
        flash('Your message could not be sent. Please try again later.', 'error')
    return render_template('contact.jinja2', form=form)
