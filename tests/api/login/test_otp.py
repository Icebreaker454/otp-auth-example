import pytest
import pyotp.totp
from starlette.responses import JSONResponse
from starlette.requests import Request

from otp_auth.auth.models import LoginAttempt


@pytest.fixture
def login_attempt(db, sample_user):
    """ A previously made login attempt which lead to OTP step """
    attempt = LoginAttempt(user=sample_user)
    db.add(attempt)
    db.commit()
    return attempt


@pytest.fixture
def otp_code(sample_user):
    return pyotp.totp.TOTP(sample_user.totp_secret).now()


@pytest.fixture
def valid_otp_data(login_attempt, otp_code):
    """ A legit identifier and code for OTP verification """
    return {"identifier": login_attempt.identifier, "code": otp_code}


async def view_session(request: Request):
    """ Utility endpoint for viewing current client's session"""
    return JSONResponse(request.session)


@pytest.fixture
def client(client, app):
    """ Client with extra route for viewing session """
    app.add_route("/view_session", view_session, methods=["GET"])
    return client


class TestLoginOTP:
    """ Test suite for OTP exchange endpoint """

    url = "/auth/otp"

    def test_valid_otp(self, client, valid_otp_data):
        """ Valid OTP request should return an OK message """
        resp = client.post(self.url, json=valid_otp_data)
        assert resp.status_code == 200
        assert resp.json()["status"] == "OK"

    def test_access_token_in_session_after_login(self, client, valid_otp_data):
        """ Access token should be present in session after login """

        resp = client.post(self.url, json=valid_otp_data)
        assert resp.status_code == 200

        session_resp = client.get("/view_session")
        assert "access_token" in session_resp.json()

    def test_invalid_otp(self, client, valid_otp_data):
        """ Incorrect OTP code should raise an error """

        valid_otp_data["code"] += "1"

        resp = client.post(self.url, json=valid_otp_data)
        assert resp.status_code == 401
        assert resp.json()["code"] == "invalid_otp"

    def test_expired_login_attempt(
        self, client, db, login_attempt, valid_otp_data, now, delta
    ):
        """ Expired login attempts should not pass OTP validation """

        login_attempt.timestamp = now() - delta(seconds=600)
        db.commit()

        resp = client.post(self.url, json=valid_otp_data)
        assert resp.status_code == 401
        assert resp.json()["code"] == "invalid_otp"
