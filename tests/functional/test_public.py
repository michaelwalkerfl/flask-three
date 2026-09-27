from webapp import mail


def test_index_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Ship your Flask app' in response.data


def test_index_page_post_not_allowed(client):
    assert client.post('/').status_code == 405


def test_about_page(client):
    response = client.get('/about')
    assert response.status_code == 200
    assert b'Principles' in response.data


def test_security_headers(client):
    response = client.get('/')
    csp = response.headers['Content-Security-Policy']
    assert "default-src 'self'" in csp
    assert 'nonce-' in csp


def test_404_page(client):
    response = client.get('/does-not-exist')
    assert response.status_code == 404
    assert b'Page not found' in response.data


def test_contact_form_sends_email(client):
    with mail.record_messages() as outbox:
        response = client.post(
            '/contact',
            data={
                'name': 'Jane',
                'email': 'jane@example.com',
                'subject': 'Hello',
                'message': 'This is a test message.',
            },
            follow_redirects=True,
        )
    assert response.status_code == 200
    assert b'Thanks for reaching out' in response.data
    assert len(outbox) == 1
    assert outbox[0].recipients == ['admin@example.com']
    assert 'jane@example.com' in outbox[0].body


def test_contact_form_validation(client):
    response = client.post('/contact', data={'name': '', 'email': 'bad'})
    assert response.status_code == 200
    assert b'Enter a valid email address.' in response.data
