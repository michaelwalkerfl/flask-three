from tests.conftest import new_user


def test_new_user(new_user):
    assert new_user.email == 'user@example.com'
    assert new_user.passwd != 'ThisIsATest'
