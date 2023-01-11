FROM python:3.11.1-alpine3.17

COPY requirements.txt /temp/requirements.txt
COPY egedoma /egedoma
WORKDIR /egedoma
EXPOSE 8000

RUN apk add postgresql-client build-base postgresql-dev

RUN pip install -r /temp/requirements.txt

RUN adduser --disabled-password egedoma-dev

USER egedoma-dev