import logging
import os

from flask import Blueprint
from flask import render_template
from flask import redirect
from flask import flash
from flask import url_for

from flask_login import login_user
from flask_login import logout_user
from flask_login import current_user
from flask_login import login_required

from dotenv import load_dotenv

from webapp.dashboard.forms import UserRegistrationForm
from webapp.dashboard.forms import UserLoginForm
from webapp.models.user import db
from webapp.models.user import User
from webapp.models.user import Role
from webapp import login_manager
from webapp import rq
from webapp.utils import send_email


load_dotenv()

dashboard = Blueprint(
    'dashboard',
    __name__,
    template_folder="templates",
    static_folder='static',
)


@dashboard.route('/signin', methods=['GET', 'POST'])
def signin():
    if current_user.is_authenticated:
        flash('You are already logged in..')
        return redirect(url_for('dashboard.index'))
    form = UserLoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(password=form.password.data):
            login_user(user)
            if user.is_admin():
                flash(f"Admin user being redirected to {url_for('admin.index')}")
                return redirect(url_for('admin.index'))
            else:
                flash(f"User being redirected to {url_for('dashboard.index')}")
                return redirect(url_for('dashboard.index'))
        flash('Invalid login.')
        return redirect(url_for('dashboard.signin'))
    return render_template('signin.jinja2', form=form)


@dashboard.route('/sign-out')
@login_required
def sign_out():
    """User sign-out login."""
    logout_user()
    return redirect(url_for('dashboard.signin'))


@dashboard.route('/registration', methods=['GET', 'POST'])
def registration():
    """User registration page."""
    form = UserRegistrationForm()
    if form.validate_on_submit():
        user_exists = User.query.filter_by(email=form.email.data).first()
        if user_exists:
            flash('Try logging in.')
        else:
            user = User()
            user.first_name = form.first_name.data
            user.last_name = form.last_name.data
            user.email = form.email.data
            user.set_password(form.password.data)
            try:
                db.session.add(user)
                db.session.commit()
            except Exception as e:
                logging.warning('Registering user in database failed: ', e)
                db.session.rollback()
                return redirect(url_for('dashboard.registration'))
            rq.get_queue().enqueue(
                send_email,
                "You have successfully registered your account.",
                "Account registration success.",
                user.email
            )
            login_user(user)
            return redirect(url_for('dashboard.index'))
    return render_template('registration.jinja2', form=form)


@dashboard.route('/', methods=['GET', 'POST'])
@login_required
def index():
    if current_user.is_admin():
        return redirect(url_for('admin.index'))
    return render_template('dashboard.jinja2', current_user=current_user)


@login_manager.user_loader
def load_user(user_id):
    """Check to see if a user is logged in on every page that is loaded."""
    return User.query.get(user_id) if user_id else None


@login_manager.unauthorized_handler
def unauthorized_user():
    """Redirect user to login page."""
    flash('You cannot access this resource unless logged in.')
    return redirect(url_for('dashboard.signin'))
