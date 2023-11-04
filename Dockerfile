# syntax=docker/dockerfile:1

FROM python:3.11

ENV POETRY_VERSION=1.5.1

RUN pip install "poetry==$POETRY_VERSION"

WORKDIR /opt/dragon_analyzer
COPY . .
RUN poetry install
EXPOSE 6301

CMD poetry run gunicorn -b "0.0.0.0:6301"