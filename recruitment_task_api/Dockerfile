FROM python:3.10-alpine

ENV PYTHONUNBUFFERED 1

## Install dependencies
RUN apk add --update --no-cache postgresql-client jpeg-dev
RUN apk add --update --no-cache --virtual .tmp-build-deps \
    gcc libc-dev libffi-dev linux-headers postgresql-dev \
    musl-dev zlib zlib-dev

WORKDIR /
COPY . .

RUN pip install -r requirements.txt --no-cache-dir

## Media dir
RUN mkdir -p /vol/web/media
RUN mkdir -p /vol/web/static
RUN adduser -D user
RUN chown -R user:user /vol/
RUN chmod -R 755 /vol

USER user
