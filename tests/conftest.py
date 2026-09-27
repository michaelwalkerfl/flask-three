import pytest

from webapp import create_app, db
from webapp.commands import get_or_create_role
from webapp.models import User


@pytest.fixture
def app():
    app = create_app('test')
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


def make_user(email='user@example.com', password='ThisIsATest', role='user', **fields):
    user = User(email=email, first_name=fields.get('first_name', 'Test'), last_name='User')
    user.set_password(password)
    user.roles.append(get_or_create_role(db, role))
    db.session.add(user)
    db.session.commit()
    return user


@pytest.fixture
def user(app):
    return make_user()


@pytest.fixture
def admin(app):
    return make_user(email='admin@example.com', role='admin', first_name='Admin')


def sign_in(client, email, password='ThisIsATest'):
    return client.post('/dashboard/signin', data={'email': email, 'password': password})
