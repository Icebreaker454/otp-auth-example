import os
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent.parent.absolute()
os.environ["PYTHONPATH"] = str(BASE_DIR)

SQLALCHEMY_DATABASE_URI = f"sqlite:///ferretgo.sqlite3"
APP_NAME = "Login OTP App"

AUTH_OTP_THRESHOLD_SECONDS = 300  # OTPs are valid for 5 mins

SECRET_KEY = os.environ.get(
    "SECRET_KEY", "default one is not too secret, but it works"
)
