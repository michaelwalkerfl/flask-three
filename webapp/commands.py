import click
import os
from flask import current_app
from flask.cli import with_appcontext
from webapp.models.user import Role
from webapp.models.user import User


@click.command('create-database')
@with_appcontext
def create_database():
    db = current_app.db
    db.drop_all()
    db.create_all()
    print('Database created successfully.')


@click.command('create-admin')
@with_appcontext
def create_admin():
    db = current_app.db
    new_admin = User()
    new_admin.first_name = 'Admin'
    new_admin.last_name = 'User'
    new_admin.email = os.environ.get('ADMIN_EMAIL', 'email@email.com')
    new_admin.set_password(os.environ.get('ADMIN_PASSWORD', 'ChangeThisPassword'))
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
        print(f'Registering admin in database failed: {e}')
        db.session.rollback()
    print('Admin created successfully.')


@click.command('create-roles')
@with_appcontext
def create_roles():
    db = current_app.db
    roles = ['admin', 'user']
    for role in roles:
        try:
            new_role = Role()
            new_role.name = role
            db.session.add(new_role)
            db.session.commit()
        except Exception as e:
            print(f'Creating role failed: {e}')
            db.session.rollback()
    print('Roles created successfully.')
