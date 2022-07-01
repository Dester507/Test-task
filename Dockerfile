# Dockerfile

# docker image
FROM python:3.9-alpine

# work dir
WORKDIR /app

# set env variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# copy dependencies
COPY requirements.txt .

# Solve uvloop issue
RUN apk add build-base \
    && apk add libffi-dev

# install dependencies
RUN pip install -r requirements.txt

COPY . .