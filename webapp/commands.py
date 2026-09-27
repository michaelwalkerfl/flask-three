import os

import click
from flask import current_app
from flask.cli import with_appcontext

from webapp.models.user import Role, User

DEFAULT_ROLES = ('admin', 'user')


def get_or_create_role(db, name):
    role = Role.query.filter_by(name=name).first()
    if not role:
        role = Role(name=name)
        db.session.add(role)
        db.session.commit()
    return role


@click.command('create-database')
@click.option('--drop', is_flag=True, help='Drop all existing tables first (destroys data).')
@with_appcontext
def create_database(drop):
    """Create database tables. Safe to run repeatedly."""
    db = current_app.db
    if drop:
        click.confirm('This will delete all data. Continue?', abort=True)
        db.drop_all()
    db.create_all()
    click.echo('Database ready.')


@click.command('create-roles')
@with_appcontext
def create_roles():
    """Create the default roles if they do not exist."""
    db = current_app.db
    for name in DEFAULT_ROLES:
        get_or_create_role(db, name)
    click.echo(f'Roles ready: {", ".join(DEFAULT_ROLES)}.')


@click.command('create-admin')
@with_appcontext
def create_admin():
    """Create the admin user from ADMIN_EMAIL / ADMIN_PASSWORD if it does not exist."""
    db = current_app.db
    email = os.environ.get('ADMIN_EMAIL', 'email@email.com')
    if User.query.filter_by(email=email).first():
        click.echo(f'Admin {email} already exists.')
        return

    admin = User(first_name='Admin', last_name='User', email=email)
    admin.set_password(os.environ.get('ADMIN_PASSWORD', 'ChangeThisPassword'))
    admin.roles.append(get_or_create_role(db, 'admin'))
    try:
        db.session.add(admin)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise click.ClickException(f'Registering admin in database failed: {e}') from e
    click.echo(f'Admin {email} created.')
