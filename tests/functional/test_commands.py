from webapp.models import Role, User


def test_setup_commands_are_idempotent(app, monkeypatch):
    monkeypatch.setenv('ADMIN_EMAIL', 'boss@example.com')
    monkeypatch.setenv('ADMIN_PASSWORD', 'BossPassword1')
    runner = app.test_cli_runner()
    for _ in range(2):
        assert runner.invoke(args=['create-database']).exit_code == 0
        assert runner.invoke(args=['create-roles']).exit_code == 0
        assert runner.invoke(args=['create-admin']).exit_code == 0
    assert Role.query.count() == 2
    admin = User.query.filter_by(email='boss@example.com').one()
    assert admin.is_admin()
    assert admin.check_password('BossPassword1')
