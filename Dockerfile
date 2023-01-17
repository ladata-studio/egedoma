FROM python:3.11.1-alpine3.17

ENV BACKEND_HOST=http://127.0.0.1
ENV TELEGRAM_BOT_HOST=https://6523-2a01-e0a-a0d-71b0-9514-d09e-df47-1f83.eu.ngrok.io
ENV HASH_LIFETIME=300

COPY requirements.txt /temp/requirements.txt
COPY egedoma /egedoma
WORKDIR /egedoma
EXPOSE 80

RUN apk add postgresql-client build-base postgresql-dev

RUN pip install -r /temp/requirements.txt

RUN adduser --disabled-password egedoma-dev

USER egedoma-dev