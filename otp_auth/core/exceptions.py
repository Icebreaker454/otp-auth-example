""" Module containing common exception class for typical LEAN FastAPI projects """
from typing import Any


class CommonError(Exception):
    code: str
    message: str
    additional: Any = None
    status: int = 400

    def content(self):
        return {
            "code": self.code,
            "message": self.message,
            "additional_info": self.additional,
        }


class ValidationError(CommonError):
    code = "validation_error"
    status = 422
    message = "The data submitted is not valid"

    def __init__(self, errors: dict):
        self.errors = errors

    @property
    def additional(self):
        return self.errors
