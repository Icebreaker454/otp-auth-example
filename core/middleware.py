from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from starlette.requests import Request

from core.exceptions import CommonError


def handle_common_error(request: Request, exc: CommonError):
    """ Handles a `CommonError` raised """
    return JSONResponse(status_code=exc.status,
                        content=jsonable_encoder(exc.content()))


def register_common_errorhandler(app: FastAPI, config):
    """ Registers a common error hander """
    app.exception_handler(CommonError)(handle_common_error)
