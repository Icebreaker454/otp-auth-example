import secrets
from datetime import datetime

import pyotp
import sqlalchemy as sa
from sqlalchemy.event import listen
from sqlalchemy.orm import relationship

import config
from auth.pwd_context import get_password_hash
from db.base_model import Base


def get_totp_secret():
    """ Function for generating a secret for TOTP algorithm """
    return pyotp.random_base32()


def hash_user_password(mapper, context, target):
    """ SQLAlchemy event hook for hashing raw passwords """
    target.hash_password()


def make_identifier():
    return secrets.token_hex(16)


class User(Base):
    """ A simple user model """

    id = sa.Column(sa.String(), primary_key=True)
    username = sa.Column(sa.String(), nullable=False, index=True)
    password = sa.Column(sa.String(), nullable=False)
    totp_secret = sa.Column(sa.String(), default=get_totp_secret, nullable=False)

    def hash_password(self):
        """ Stores hashed password into DB instead of the raw one """
        self.password = get_password_hash(self.password)


class LoginAttempt(Base):
    """ Describes a single registration attempt with an identifier """

    id = sa.Column(sa.String(), primary_key=True)
    identifier = sa.Column(
        sa.String(), index=True, nullable=False, default=make_identifier
    )
    timestamp = sa.Column(sa.DateTime(), default=datetime.utcnow)

    user_id = sa.Column(sa.Integer(), sa.ForeignKey("user.id"), nullable=False)
    user = relationship(User, uselist=False)

    # Possibly, add more meta info ? status, IP, etc

    def is_valid(self) -> bool:
        return (
            datetime.utcnow() - self.timestamp
        ).seconds < config.AUTH_OTP_THRESHOLD_SECONDS


listen(User, "before_insert", hash_user_password)
