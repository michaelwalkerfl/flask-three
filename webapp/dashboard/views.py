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

from webapp.dashboard.forms import UserRegistrationForm
from webapp.dashboard.forms import UserLoginForm
from webapp.models.user import db
from webapp.models.user import User
from webapp.models.user import Role
from webapp import login_manager
from webapp.utils import parse_env

parse_env()

dashboard = Blueprint(
    'dashboard',
    __name__,
    template_folder="templates",
    static_folder='static',
)


@dashboard.route('/signin', methods=['GET', 'POST'])
def signin():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))
    form = UserLoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_passwd(passwd=form.passwd.data):
            login_user(user)
            if user.is_admin():
                return redirect(url_for('dashboard.admin_dashboard'))
            else:
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


@dashboard.cli.command("create-database")
def create_database():
    db.create_all()
    print("Database created successfully.")


@dashboard.cli.command("create-roles")
def create_roles():
    admin_role = Role(name="admin")
    user_role = Role(name="user")
    try:
        db.session.add(admin_role)
        db.session.add(user_role)
        db.session.commit()
    except Exception as e:
        logging.warning("Creating roles failed: ", e)
        db.session.rollback()
    print("Roles created successfully.")


@dashboard.cli.command('create-admin')
def create():
    new_admin = User(
        first_name="Admin",
        last_name="User",
        email=os.environ.get('ADMIN_EMAIL'),
    )
    new_admin.set_passwd(os.environ.get('ADMIN_PASSWORD', 'ChangeThisPassword'))
    admin_role = Role.query.filter_by(name='admin').first()
    if not admin_role:
        admin_role = Role(name='admin')
        db.session.add(admin_role)
        db.session.commit()
    new_admin.roles.append(admin_role)
    try:
        db.session.add(new_admin)
        db.session.commit()
    except Exception as e:
        logging.warning('Registering admin in database failed: ', e)
        db.session.rollback()
    print(f"Admin created successfully.")


@dashboard.route('/registration', methods=['GET', 'POST'])
def registration():
    """User registration page."""
    form = UserRegistrationForm()
    if form.validate_on_submit():
        user_exists = User.query.filter_by(email=form.email.data).first()
        if user_exists:
            flash('Try logging in.')
        else:
            user = User(
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                email=form.email.data,
            )
            user.set_passwd(form.passwd.data)
            try:
                db.session.add(user)
                db.session.commit()
            except Exception as e:
                logging.warning('Registering user in database failed: ', e)
                db.session.rollback()
                return redirect(url_for('dashboard.registration'))
            login_user(user)
            return redirect(url_for('dashboard.index'))
    return render_template('registration.jinja2', form=form)


@dashboard.route('/', methods=['GET', 'POST'])
@login_required
def index():
    if current_user.is_admin():
        return redirect()
    return render_template('dashboard.jinja2', current_user=current_user)


@login_manager.user_loader
def load_user(user_id):
    """Check to see if a user is logged in on every page that is loaded."""
    if user_id:
        return User.query.get(user_id)
    else:
        return None


@login_manager.unauthorized_handler
def unauthorized_user():
    """Redirect user to login page."""
    flash('You cannot access this resource unless logged in.')
    return redirect(url_for('dashboard.signin'))
