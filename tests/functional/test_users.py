
def test_index_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Welcome' in response.data


def test_index_page_post(client):
    response = client.post('/')
    assert response.status_code == 405
    assert b'Welcome' not in response.data


def test_registration_page(client):
    response = client.get('/dashboard/registration')
    assert response.status_code == 200
    assert b'SIGN UP' in response.data
