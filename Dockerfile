FROM python:3.8-alpine

RUN apk add --no-cache \
    gcc \
    python3-dev \
    build-base \
    libffi-dev \
    libxml2-dev \
    musl-dev \
    libxslt-dev \
    curl

COPY ./Pipfile* /

RUN pip install -U pip setuptools pipenv
RUN pipenv install --deploy --system

COPY . /src
WORKDIR /src

EXPOSE 5000

CMD uvicorn main:app --host 0.0.0.0 --port 5000 --log-level=debug
