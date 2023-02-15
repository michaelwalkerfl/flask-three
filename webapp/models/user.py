import datetime

from webapp import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash


class User(UserMixin, db.Model):
    """User database model."""

    __tablename__ = 'users'
    id = db.Column(
        db.Integer,
        primary_key=True,
    )
    first_name = db.Column(
        db.String(50),
        nullable=False,
        unique=False,
    )
    last_name = db.Column(
        db.String(50),
        nullable=False,
        unique=False,
    )
    email = db.Column(
        db.String(64),
        unique=True,
        nullable=False,
    )
    passwd = db.Column(
        db.String(200),
        primary_key=False,
        unique=False,
        nullable=False,
    )
    created_on = db.Column(
        db.DateTime(timezone=True),
        index=False,
        unique=False,
        server_default=func.now(),
    )

    last_login = db.Column(
        db.DateTime,
        index=False,
        unique=False,
        nullable=True,
    )

    role =

    def set_passwd(self, passwd):
        """Create password hash."""
        self.passwd = generate_password_hash(
            passwd,
            method='sha256'
        )

    def check_passwd(self, passwd):
        """Check password hash."""
        return check_password_hash(
            self.passwd, passwd)

    def __repr__(self):
        return '<User {}>'.format(self.email)
