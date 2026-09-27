import logging
import os

import redis
from flask import current_app, has_app_context
from flask_mail import Message
from rq import Queue

logger = logging.getLogger(__name__)


def register_template_utils(app):
    """Register Jinja2 helpers."""

    @app.template_filter('datetime')
    def format_datetime(value, fmt='%b %d, %Y'):
        return value.strftime(fmt) if value else 'Never'

    @app.template_filter('initials')
    def initials(user):
        parts = [user.first_name or '', user.last_name or '']
        letters = ''.join(part[:1] for part in parts if part).upper()
        return letters or user.email[:1].upper()


def _deliver(subject: str, body: str, to: str):
    from webapp import mail

    msg = Message(subject=subject, recipients=[to], body=body)
    mail.send(msg)


def send_email(subject: str, body: str, to: str):
    """Send an email. Runs inside an RQ worker or an existing app context."""
    if has_app_context():
        _deliver(subject, body, to)
        return

    from webapp import create_app

    app = create_app(os.getenv('APP_ENV', 'default'))
    with app.app_context():
        _deliver(subject, body, to)


def queue_email(subject: str, body: str, to: str):
    """Queue an email on RQ, or send it inline when EMAIL_ASYNC is disabled."""
    try:
        if current_app.config['EMAIL_ASYNC']:
            connection = redis.from_url(current_app.config['RQ_REDIS_URL'])
            queue = Queue(current_app.config['RQ_QUEUE'], connection=connection)
            queue.enqueue(send_email, subject, body, to)
        else:
            send_email(subject, body, to)
    except Exception:
        logger.exception('Failed to send email to %s', to)
        return False
    return True
