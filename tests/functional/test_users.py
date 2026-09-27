from tests.conftest import sign_in
from webapp import db, mail
from webapp.models import User


def test_registration_page(client):
    response = client.get('/dashboard/registration')
    assert response.status_code == 200
    assert b'Create your account' in response.data


def test_registration_creates_user_and_sends_email(client):
    with mail.record_messages() as outbox:
        response = client.post(
            '/dashboard/registration',
            data={
                'first_name': 'Ada',
                'last_name': 'Lovelace',
                'email': 'Ada@Example.com',
                'password': 'SuperSecret1',
                'password_confirm': 'SuperSecret1',
            },
            follow_redirects=True,
        )
    assert response.status_code == 200
    assert b'Hello, Ada' in response.data
    user = User.query.filter_by(email='ada@example.com').one()
    assert user.has_role('user')
    assert len(outbox) == 1


def test_registration_rejects_duplicate_email(client, user):
    response = client.post(
        '/dashboard/registration',
        data={
            'first_name': 'Dup',
            'last_name': 'User',
            'email': user.email,
            'password': 'SuperSecret1',
            'password_confirm': 'SuperSecret1',
        },
    )
    assert b'already exists' in response.data
    assert User.query.count() == 1


def test_signin_success_updates_last_login(client, user):
    response = sign_in(client, user.email)
    assert response.status_code == 302
    assert response.headers['Location'].endswith('/dashboard/')
    assert db.session.get(User, user.id).last_login is not None


def test_signin_invalid_password(client, user):
    response = sign_in(client, user.email, 'wrong-password')
    assert response.status_code == 200
    assert b'Invalid email or password.' in response.data


def test_signin_honours_safe_next_only(client, user):
    response = client.post(
        '/dashboard/signin?next=https://evil.example.com',
        data={'email': user.email, 'password': 'ThisIsATest'},
    )
    assert response.headers['Location'].endswith('/dashboard/')


def test_dashboard_requires_login(client):
    response = client.get('/dashboard/')
    assert response.status_code == 302
    assert '/dashboard/signin' in response.headers['Location']


def test_user_dashboard(client, user):
    sign_in(client, user.email)
    response = client.get('/dashboard/')
    assert response.status_code == 200
    assert user.email.encode() in response.data


def test_user_cannot_access_admin(client, user):
    sign_in(client, user.email)
    assert client.get('/administrator/').status_code == 403


def test_admin_dashboard(client, admin, user):
    response = sign_in(client, admin.email)
    assert response.headers['Location'].endswith('/administrator/')
    response = client.get('/administrator/')
    assert response.status_code == 200
    assert b'Total users' in response.data
    assert user.email.encode() in response.data


def test_sign_out(client, user):
    sign_in(client, user.email)
    response = client.get('/dashboard/sign-out')
    assert response.status_code == 302
    assert client.get('/dashboard/').status_code == 302
