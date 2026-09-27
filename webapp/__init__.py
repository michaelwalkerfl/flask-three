import os
from datetime import UTC, datetime

from flask import Flask, render_template
from flask_login import LoginManager
from flask_mail import Mail
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_talisman import Talisman
from flask_wtf import CSRFProtect

from config import config as cfg

base_directory = os.path.abspath(os.path.dirname(__file__))

db = SQLAlchemy()
csrf = CSRFProtect()
mail = Mail()
sess = Session()

login_manager = LoginManager()
login_manager.session_protection = 'basic'
login_manager.login_view = 'dashboard.signin'


def create_app(config_name=None):
    """Application factory. Falls back to the APP_ENV environment variable."""
    config_name = config_name or os.getenv('APP_ENV', 'default')

    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object(cfg[config_name])
    cfg[config_name].init_app(app)

    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    sess.init_app(app)
    csrf.init_app(app)

    cdn = app.config['FONT_AWESOME_CDN']
    csp = {
        'default-src': "'self'",
        'script-src': "'self'",
        'img-src': "'self' data: blob:",
        'style-src': ["'self'", cdn],
        'font-src': ["'self'", cdn],
    }
    Talisman(
        app,
        force_https=app.config['FORCE_HTTPS'],
        content_security_policy=csp,
        content_security_policy_nonce_in=['script-src'],
    )
    app.db = db

    from webapp import models  # noqa: F401
    from webapp.commands import create_admin, create_database, create_roles

    app.cli.add_command(create_database)
    app.cli.add_command(create_admin)
    app.cli.add_command(create_roles)

    register_blueprints(app)
    register_error_handlers(app)

    @app.context_processor
    def inject_globals():
        return {'current_year': datetime.now(UTC).year}

    return app


def register_blueprints(app):
    from .utils import register_template_utils

    register_template_utils(app)

    from .public import public as public_blueprint

    app.register_blueprint(public_blueprint)

    from .dashboard import dashboard as dashboard_blueprint

    app.register_blueprint(dashboard_blueprint, url_prefix='/dashboard')

    from .admin import admin as admin_blueprint

    app.register_blueprint(admin_blueprint, url_prefix='/administrator')


def register_error_handlers(app):
    messages = {
        403: ('Access denied', 'You do not have permission to view this page.'),
        404: ('Page not found', 'The page you are looking for does not exist or has moved.'),
        500: ('Something went wrong', 'An unexpected error occurred. Please try again.'),
    }

    def make_handler(code):
        def handler(error):
            if code == 500:
                db.session.rollback()
            title, message = messages[code]
            return render_template('error.jinja2', code=code, title=title, message=message), code

        return handler

    for code in messages:
        app.register_error_handler(code, make_handler(code))
