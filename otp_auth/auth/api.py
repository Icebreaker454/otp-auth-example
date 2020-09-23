import secrets

import qrcode
from fastapi import APIRouter, Depends, Response
from lxml import etree
from qrcode.image.svg import SvgImage
from starlette.requests import Request

from otp_auth.auth.managers import LoginManager, TOTPManager
from otp_auth.auth.models import User
from otp_auth.auth.schemas import LoginIn, LoginOut, VerifyOTPIn, VerifyOTPOut
from otp_auth.db.middleware import get_db
from otp_auth.db.session import Session

router = APIRouter()


@router.post("/login", response_model=LoginOut)
def login(login_meta: LoginIn, db: Session = Depends(get_db)):
    """ Login user """
    mgr = LoginManager()
    login_attempt = mgr.login(db, login_meta.username, login_meta.password)
    return {"identifier": login_attempt.identifier}


@router.post("/otp", response_model=VerifyOTPOut)
def verify_otp(request: Request, body: VerifyOTPIn, db: Session = Depends(get_db)):
    """ Verify OTP for a previous login attempt """
    mgr = LoginManager()
    mgr.verify_otp(db, body.identifier, body.code)
    request.session["access_token"] = secrets.token_hex(16)
    return {"status": "OK"}


@router.get("/otp/setup")
def setup_otp(db: Session = Depends(get_db)):
    """ Test route for displaying QR code for Google Authenticator """

    # Assume this user exists, it's just a test anyway
    user = db.query(User).filter_by(username="icebreaker").first()


    img = qrcode.make(TOTPManager(user).provision(), image_factory=SvgImage)

    rendered_svg = etree.tostring(img.get_image()).decode()

    html = f"""
    <h1>Here is your QR code for GA</h1>
    <p>
      {rendered_svg}
    </p>
    """

    return Response(content=html)
