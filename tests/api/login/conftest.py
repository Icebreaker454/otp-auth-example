import pytest

from otp_auth.auth.models import User


@pytest.fixture
def sample_user(db):
    user = User(username="icebreaker", password="swordsfish")
    db.add(user)
    db.commit()
    return user
