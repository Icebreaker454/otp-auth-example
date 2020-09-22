from fastapi import APIRouter

from auth.managers import LoginManager
from auth.schemas import LoginIn, LoginOut, VerifyOTPIn, VerifyOTPOut


router = APIRouter()


@router.post("/login", response_model=LoginOut)
def login(login_meta: LoginIn):
    """ Login user """
    mgr = LoginManager()
    login_attempt = mgr.login(login_meta.username, login_meta.password)
    return {"identifier": login_attempt.identifier}


@router.post("/otp", response_model=VerifyOTPOut)
def verify_otp():
    return {}
