from webapp import db
from flask_login import UserMixin
from flask_login import current_user
from sqlalchemy.sql import func
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash


class User(UserMixin, db.Model):
    """User database model."""

    __tablename__ = 'user'
    id = db.Column(
        db.Integer,
        primary_key=True,
    )
    first_name = db.Column(
        db.String(50),
        unique=False,
    )
    last_name = db.Column(
        db.String(50),
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

    roles = db.relationship('Role', secondary='user_roles', backref=db.backref('users', lazy='dynamic'))

    def is_authenticated(self):
        from flask_login import current_user
        return current_user.is_authenticated

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

    @classmethod
    def is_admin(cls):
        return 'admin' in [role.name for role in current_user.roles]

    def __repr__(self):
        return '<User {}>'.format(self.email)


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)


class UserRoles(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), primary_key=True)
