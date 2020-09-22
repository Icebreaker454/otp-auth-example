from pydantic import BaseModel


class LoginIn(BaseModel):
    username: str
    password: str


class LoginOut(BaseModel):
    identifier: str


class VerifyOTPIn(BaseModel):
    identifier: str
    code: str


class VerifyOTPOut(BaseModel):
    access_token: str
