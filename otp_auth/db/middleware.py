from starlette.requests import Request

from otp_auth.db.session import Session


async def db_session_middleware(request: Request, call_next):
    """ Middleware for adding a DB session to current request """
    request.state.db = Session()
    response = await call_next(request)
    request.state.db.close()
    return response


def get_db(request: Request) -> Session:
    """ FastAPI Depends-like function for getting current db session """
    return request.state.db
