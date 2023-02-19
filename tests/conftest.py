import pytest
from webapp import create_app, db
from webapp.models import User


@pytest.fixture(scope='session')
def app():
    app = create_app('test')
    with app.app_context():
        db.create_all()

    yield app

    with app.app_context():
        db.drop_all()


@pytest.fixture(scope='function')
def client(app):
    with app.test_client() as client:
        with app.app_context():
            yield client

            db.session.rollback()


@pytest.fixture(scope='function')
def session(app):
    with app.app_context():
        db.session.begin_nested()
        yield db.session
        db.session.rollback()
        db.session.expunge_all()


@pytest.fixture(scope='function', autouse=True)
def rollback_transitions(session):
    yield
    session.rollback()


@pytest.fixture(scope='function', autouse=True)
def commit_changes(session):
    yield
    session.commit()


@pytest.fixture(scope='module')
def new_user():
    user = User(email='user@example.com')
    user.set_passwd(passwd='ThisIsATest')
    return user
