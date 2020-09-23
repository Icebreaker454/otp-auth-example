# OTP Authentication example in FastAPI

This is a simple example of how to authenticate a user with OTP,
featuring Google Authenticator or other applications with TOTP support.

## Setup

For local startup purposes, a `docker-compose.yml` file is generated.
Simply do a 
```
$ docker-compose up
```
and that should start the `uvicorn` server locally at port 8000.

You can test that it works using the test credentials

## Development

The project utilizes [Pipenv](https://pypi.org/project/pipenv/) as the package management tool.
Ensure you have the dev dependencies installed by running

```
$ pipenv install --dev
```

Run tests using the `pytest` command:
```
$ pytest 
```

Basic code style is enforced via [Black](https://pypi.org/project/black/)
Consider running `$ black .` before pushing contributions.

## DB migrations

This project features [Alembic](https://pypi.org/project/alembic) as the DB migration toolkit.
Whenever your contributions imply changing the DB structure, ensure the migrations are
properly generated. Execute the following from project root:
```
$ PYTHONPATH=`pwd` alembic revision --autogenerate -m "<Message with changes>"
```

