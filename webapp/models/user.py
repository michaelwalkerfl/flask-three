from flask_login import UserMixin
from sqlalchemy.sql import func
from werkzeug.security import check_password_hash, generate_password_hash

from webapp import db


class User(UserMixin, db.Model):
    """User database model."""

    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    email = db.Column(db.String(254), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    created_on = db.Column(db.DateTime(timezone=True), server_default=func.now())
    last_login = db.Column(db.DateTime(timezone=True), nullable=True)

    roles = db.relationship(
        'Role', secondary='user_roles', backref=db.backref('users', lazy='dynamic')
    )

    @property
    def full_name(self):
        name = ' '.join(part for part in (self.first_name, self.last_name) if part)
        return name or self.email

    def set_password(self, password):
        """Create password hash."""
        self.password = generate_password_hash(password, method='scrypt')

    def check_password(self, password):
        """Check password hash."""
        return check_password_hash(self.password, password)

    def has_role(self, name):
        return any(role.name == name for role in self.roles)

    def is_admin(self):
        return self.has_role('admin')

    def __repr__(self):
        return f'<User {self.email}>'


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return f'<Role {self.name}>'


class UserRoles(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), primary_key=True)
