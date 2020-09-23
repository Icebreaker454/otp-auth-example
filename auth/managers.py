from typing import Optional

import pyotp
import pyotp.totp

import config
from auth.exceptions import InvalidOTP, InvalidUserCredentials
from auth.models import LoginAttempt, User
from auth.pwd_context import verify_password


class LoginManager:
    """ Manager for the login process. Utilizes two-step TOTP checking """

    def authenticate(self, session, username, password) -> Optional[User]:
        """ Fetches the user from DB and validates password """
        user = session.query(User).filter_by(username=username).first()
        if not user or not verify_password(password, user.password):
            return None
        return user

    def login(self, session, username, password) -> LoginAttempt:
        """ Tries to log the user in """

        user = self.authenticate(session, username, password)
        if not user:
            raise InvalidUserCredentials

        attempt = LoginAttempt(user=user)
        session.add(attempt)
        session.commit()
        return attempt

    def verify_otp(self, session, identifier, code):
        """ Verifies OTP for a single login attempt """
        attempt = session.query(LoginAttempt).filter_by(identifier=identifier).first()
        conditions = [
            attempt,
            attempt.is_valid(),
            TOTPManager(attempt.user).verify(code),
        ]
        if not all(conditions):
            raise InvalidOTP
        return True


class TOTPManager:
    """ Manager for TOTP verification """

    def __init__(self, user: User):
        """ Initializes TOTP manager on given user """
        self.user = user

    def __initialize_totp(self) -> pyotp.totp.TOTP:
        """ Initializes a TOTP for given user """
        return pyotp.totp.TOTP(self.user.totp_secret)

    def provision(self) -> str:
        """ Returns a TOTP provisioning url for Google authenticator """
        totp = self.__initialize_totp()
        return totp.provisioning_uri(self.user.username, issuer_name=config.APP_NAME)

    def verify(self, code) -> bool:
        """ Checks TOTP code against user secret """
        totp = self.__initialize_totp()
        return totp.verify(code)
