FROM python:3.12

WORKDIR /app

RUN apt-get update
RUN pip3 install poetry==1.8.3
COPY poetry.lock /app/
COPY pyproject.toml /app/
RUN poetry install

COPY .env /app
COPY src/ /app
