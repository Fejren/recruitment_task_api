FROM python:3.10-alpine

ENV PYTHONUNBUFFERED 1
RUN pip install --upgrade pip

## Install dependencies
RUN apk add --update --no-cache postgresql-client jpeg-dev
RUN apk add --update --no-cache --virtual .tmp-build-deps \
    gcc libc-dev libffi-dev linux-headers postgresql-dev \
    musl-dev zlib zlib-dev

RUN mkdir /recruitment_task_api
WORKDIR /recruitment_task_api
COPY ./recruitment_task_api /recruitment_task_api

RUN pip install -r requirements.txt --no-cache-dir
