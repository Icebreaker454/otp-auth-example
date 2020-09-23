import os

SQLALCHEMY_DATABASE_URI = "sqlite:///ferretgo.sqlite3"
APP_NAME = "Login OTP App"

AUTH_OTP_THRESHOLD_SECONDS = 300  # OTPs are valid for 5 mins

SECRET_KEY = os.environ.get(
    "SECRET_KEY", "default one is not too secret, but it works"
)
