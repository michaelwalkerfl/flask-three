from webapp.models import User


def test_password_is_hashed():
    user = User(email='user@example.com')
    user.set_password('ThisIsATest')
    assert user.password != 'ThisIsATest'
    assert user.check_password('ThisIsATest')
    assert not user.check_password('wrong')


def test_roles(user, admin):
    assert not user.is_admin()
    assert user.has_role('user')
    assert admin.is_admin()


def test_full_name_falls_back_to_email():
    assert User(email='a@b.com').full_name == 'a@b.com'
    assert User(email='a@b.com', first_name='Ada', last_name='Lovelace').full_name == 'Ada Lovelace'
