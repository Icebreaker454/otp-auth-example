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

## See how it works

An example account should be created with the following credentials:

*Username*: icebreaker

*Password*: swordsfish

Firstly, go to `https://localhost:5000/auth/otp/setup`, and scan the QR code via Google Authenticator.

Then, issue a login request as follows:
```shell
$ http post localhost:8000/auth/login username=icebreaker password=swordsfish 
HTTP/1.1 200 OK
content-length: 49
content-type: application/json
date: Wed, 23 Sep 2020 19:36:44 GMT
server: uvicorn

{
    "identifier": "c7ab2915829b798480ab40a13eae268a"
}

```
You will get a login session identifier for the next request.

```shell
$ http post localhost:8000/auth/otp identifier=c7ab2915829b798480ab40a13eae268a code=738664
HTTP/1.1 200 OK
content-length: 15
content-type: application/json
date: Wed, 23 Sep 2020 19:40:24 GMT
server: uvicorn
set-cookie: session=eyJhY2Nlc3NfdG9rZW4iOiAiYjA0ZGRjOTJlOWJhMDZmYzZjZDUxMzg2MmNlMWY4MjEifQ==.X2ukqA.GWIVzY2nL46xfvKASbcLNpaHRxQ; path=/; Max-Age=1209600; httponly; samesite=lax

{
    "status": "OK"
}
```
As you can see, a secure cookie has been set meaning that the user is now authenticated for further requests.

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

