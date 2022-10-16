import os

from flask import Flask
from flask_login import LoginManager
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_talisman import Talisman
from flask_wtf import CSRFProtect

from config import config as cfg

base_directory = os.path.abspath(os.path.dirname(__file__))

db = SQLAlchemy()
csrf = CSRFProtect()

login_manager = LoginManager()
login_manager.session_protection = 'basic'
login_manager.login_view = 'dashboard.login'

sess = Session()


def create_app(config):
    app = Flask(__name__, instance_relative_config=False)

    config_type = config
    if not isinstance(config, str):
        config_type = os.getenv('FLASK_ENV', 'default')

    app.config.from_object(cfg[config_type])
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    cfg[config_type].init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    sess.init_app(app)
    csrf.init_app(app)
    Talisman(app)

    with app.app_context():
        from .utils import register_template_utils
        register_template_utils(app)

        from .public import public as public_blueprint
        app.register_blueprint(public_blueprint)

        from .dashboard import dashboard as dashboard_blueprint
        app.register_blueprint(dashboard_blueprint, url_prefix='/dashboard')

        from .admin import admin as admin_dashboard
        app.register_blueprint(admin_dashboard, url_prefix='/administrator')

        db.create_all()

        return app
