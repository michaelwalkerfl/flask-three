import os

import redis
from cachelib import SimpleCache
from dotenv import load_dotenv

base_directory = os.path.abspath(os.path.dirname(__file__))

load_dotenv(os.path.join(base_directory, 'config.env'))
load_dotenv()

DEFAULT_SECRET_KEY = 'SET_YOUR_SECRET_FLASK_THREE_KEY'


def env_bool(name, default=False):
    value = os.environ.get(name)
    if value is None:
        return default
    return value.strip().lower() in ('1', 'true', 'yes', 'on')


class Config:
    # Flask
    APP_NAME = os.environ.get('APP_NAME', 'Flask3')
    REPOSITORY_URL = os.environ.get(
        'REPOSITORY_URL', 'https://github.com/michaelwalkerfl/flask-three'
    )
    SECRET_KEY = os.environ.get('FLASK_SECRET_KEY', DEFAULT_SECRET_KEY)
    ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL')

    # Security headers (Flask-Talisman)
    FORCE_HTTPS = env_bool('FORCE_HTTPS', True)
    FONT_AWESOME_CDN = os.environ.get('FONT_AWESOME_CDN', 'https://cdnjs.cloudflare.com')
    FONT_AWESOME_CSS = os.environ.get(
        'FONT_AWESOME_CSS',
        FONT_AWESOME_CDN + '/ajax/libs/font-awesome/7.3.1/css/all.min.css',
    )
    FONT_AWESOME_SRI = os.environ.get(
        'FONT_AWESOME_SRI',
        'sha512-QeR2VH+lsBE5LSAe1Q5EnTBbe7XTBubt8dG93Y7gidSgdMCr8nVqKcfKAMyN96SV8KDbZVTDXChatu5G2KQGzg==',
    )

    # Database
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Flask-Mail
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.sendgrid.net')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', 587))
    MAIL_USE_TLS = env_bool('MAIL_USE_TLS', True)
    MAIL_USE_SSL = env_bool('MAIL_USE_SSL', False)
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER', ADMIN_EMAIL)

    # Flask-Session
    SESSION_TYPE = os.environ.get('SESSION_TYPE', 'redis')
    SESSION_REDIS = redis.from_url(os.environ.get('SESSION_REDIS', 'redis://redis:6379/0'))

    # Background jobs (RQ)
    RQ_REDIS_URL = os.environ.get(
        'RQ_REDIS_URL', os.environ.get('SESSION_REDIS', 'redis://redis:6379/0')
    )
    RQ_QUEUE = os.environ.get('RQ_QUEUE', 'default')
    EMAIL_ASYNC = env_bool('EMAIL_ASYNC', True)

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DEVELOPMENT_DATABASE',
        'sqlite:///' + os.path.join(base_directory, 'development-database.sqlite'),
    )

    @classmethod
    def init_app(cls, app):
        app.logger.info('Application is in development mode.')


class TestsConfig(Config):
    TESTING = True
    FORCE_HTTPS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE', 'sqlite://')
    WTF_CSRF_ENABLED = False
    SESSION_TYPE = 'cachelib'
    SESSION_CACHELIB = SimpleCache()
    EMAIL_ASYNC = False
    MAIL_DEFAULT_SENDER = 'noreply@example.com'
    ADMIN_EMAIL = 'admin@example.com'


class ProductionConfig(Config):
    DEBUG = False
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'PRODUCTION_DATABASE',
        'sqlite:///' + os.path.join(base_directory, 'production-database.sqlite'),
    )

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)
        if app.config['SECRET_KEY'] == DEFAULT_SECRET_KEY:
            raise RuntimeError('FLASK_SECRET_KEY must be set in production.')


class UbuntuConfig(ProductionConfig):
    @classmethod
    def init_app(cls, app):
        ProductionConfig.init_app(app)

        import logging
        from logging.handlers import SysLogHandler

        syslog_handler = SysLogHandler()
        syslog_handler.setLevel(logging.WARNING)
        app.logger.addHandler(syslog_handler)


config = {
    'development': DevelopmentConfig,
    'test': TestsConfig,
    'production': ProductionConfig,
    'ubuntu': UbuntuConfig,
    'default': DevelopmentConfig,
}
