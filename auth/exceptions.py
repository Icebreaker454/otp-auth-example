from core.exceptions import CommonError


class InvalidUserCredentials(CommonError):
    code = "invalid_user_credentials"
    message = "No user can be found matching provided credentials"
    status = 401


class InvalidOTP(CommonError):
    code = "inivalid_otp"
    message = "The OTP provided is not valid"
    status = 401
