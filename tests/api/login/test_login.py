import pytest

from otp_auth.auth.models import LoginAttempt


@pytest.fixture
def no_user():
    """ Fixture describing login creds of nonexistent user """
    return {"username": "mr.incognito", "password": "donthaveone"}


@pytest.fixture
def invalid_password():
    """ Fixture describing login creds  with invalid password """
    return {"username": "icebreaker", "password": "donthaveone"}


@pytest.fixture
def valid_login_data(sample_user):
    """ Creds valid for login """
    return {"username": sample_user.username, "password": "swordsfish"}


class TestLogin:
    """ Test suite for login endpoint """

    url = "/auth/login"

    @pytest.mark.parametrize("invalid_creds_fixture", ("no_user", "invalid_password"))
    def test_invalid_credentials(self, request, client, invalid_creds_fixture):
        """ Invalid credentials should return a defined error """
        invalid_creds = request.getfixturevalue(invalid_creds_fixture)

        resp = client.post(self.url, json=invalid_creds)
        assert resp.status_code == 401
        assert resp.json()["code"] == "invalid_user_credentials"

    def test_post_required(self, client, valid_login_data):
        """ Only POST requests should be used for credential submission """
        resp = client.get(self.url, json=valid_login_data)
        assert resp.status_code == 405

    def test_successful_login(self, client, db, valid_login_data):
        """ Login should produce a login attempt """

        assert db.query(LoginAttempt).count() == 0

        resp = client.post(self.url, json=valid_login_data)
        assert resp.status_code == 200
        assert "identifier" in resp.json()

        attempt = db.query(LoginAttempt).first()
        assert attempt
        assert attempt.identifier == resp.json()["identifier"]
        assert attempt.is_valid()
