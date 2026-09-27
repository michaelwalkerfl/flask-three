import logging
from datetime import UTC, datetime
from urllib.parse import urlsplit

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user

from webapp import db, login_manager
from webapp.commands import get_or_create_role
from webapp.dashboard.forms import UserLoginForm, UserRegistrationForm
from webapp.models.user import User
from webapp.utils import queue_email

logger = logging.getLogger(__name__)

dashboard = Blueprint(
    'dashboard',
    __name__,
    template_folder='templates',
    static_folder='static',
)


def home_for(user):
    return url_for('admin.index') if user.is_admin() else url_for('dashboard.index')


def safe_next_url():
    """Return the ?next= target only if it is a local path."""
    target = request.args.get('next', '')
    parts = urlsplit(target)
    if target.startswith('/') and not target.startswith('//') and not parts.netloc:
        return target
    return None


@dashboard.route('/signin', methods=['GET', 'POST'])
def signin():
    if current_user.is_authenticated:
        return redirect(home_for(current_user))
    form = UserLoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.strip().lower()).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            user.last_login = datetime.now(UTC)
            db.session.commit()
            flash(f'Welcome back, {user.first_name or user.email}.', 'success')
            return redirect(safe_next_url() or home_for(user))
        flash('Invalid email or password.', 'error')
    return render_template('signin.jinja2', form=form)


@dashboard.route('/sign-out')
@login_required
def sign_out():
    """User sign-out."""
    logout_user()
    flash('You have been signed out.', 'info')
    return redirect(url_for('dashboard.signin'))


@dashboard.route('/registration', methods=['GET', 'POST'])
def registration():
    """User registration page."""
    if current_user.is_authenticated:
        return redirect(home_for(current_user))
    form = UserRegistrationForm()
    if form.validate_on_submit():
        email = form.email.data.strip().lower()
        if User.query.filter_by(email=email).first():
            flash('An account with that email already exists. Try signing in.', 'error')
            return render_template('registration.jinja2', form=form)

        user = User(
            first_name=form.first_name.data.strip(),
            last_name=form.last_name.data.strip(),
            email=email,
        )
        user.set_password(form.password.data)
        user.roles.append(get_or_create_role(db, 'user'))
        try:
            db.session.add(user)
            db.session.commit()
        except Exception:
            logger.exception('Registering user in database failed')
            db.session.rollback()
            flash('Registration failed. Please try again.', 'error')
            return render_template('registration.jinja2', form=form)

        queue_email(
            'Account registration success.',
            'You have successfully registered your account.',
            user.email,
        )
        login_user(user)
        flash('Your account has been created.', 'success')
        return redirect(url_for('dashboard.index'))
    return render_template('registration.jinja2', form=form)


@dashboard.route('/', methods=['GET'])
@login_required
def index():
    if current_user.is_admin():
        return redirect(url_for('admin.index'))
    return render_template('dashboard.jinja2')


@login_manager.user_loader
def load_user(user_id):
    """Load the logged-in user for each request."""
    return db.session.get(User, int(user_id)) if user_id else None


@login_manager.unauthorized_handler
def unauthorized_user():
    """Redirect anonymous users to the sign-in page."""
    flash('Please sign in to access that page.', 'info')
    return redirect(url_for('dashboard.signin', next=request.full_path.rstrip('?')))
