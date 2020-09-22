from fastapi import APIRouter, Depends, Response
import qrcode

from auth.managers import LoginManager, TOTPManager
from auth.models import User
from auth.schemas import LoginIn, LoginOut, VerifyOTPIn, VerifyOTPOut
from db.middleware import get_db
from db.session import Session


router = APIRouter()


@router.post("/login", response_model=LoginOut)
def login(login_meta: LoginIn, db: Session = Depends(get_db)):
    """ Login user """
    mgr = LoginManager()
    login_attempt = mgr.login(db, login_meta.username, login_meta.password)
    return {"identifier": login_attempt.identifier}


@router.post("/otp", response_model=VerifyOTPOut)
def verify_otp(body: VerifyOTPIn, db: Session = Depends(get_db)):
    """ Verify OTP for a previous login attempt """
    mgr = LoginManager()
    mgr.verify_otp(db, body.identifier, body.code)
    return {"access_token": "OK"}


@router.get("/otp/setup")
def setup_otp(db: Session = Depends(get_db)):
    """ Test route for displaying QR code for Google Authenticator """
    user = db.query(User).filter_by(username="icebreaker").first()
    # Assume this user exists, it's just a test anyway
    img = qrcode.make(TOTPManager(user).provision())

    import base64
    from io import BytesIO
    buffered = BytesIO()
    img.save(buffered)

    b64_image = base64.b64encode(buffered.getvalue()).decode()

    html = f"""
    <h1>Here is your QR code for GA</h1>
    <p>
      <img alt="QR Code" src="data:image/png;base64,{b64_image}" />
    </p>
    """

    return Response(content=html)
