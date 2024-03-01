FROM python:3.11.5-alpine

MAINTAINER jaehyeonJeon


COPY . /code/
WORKDIR /code/backend/server

RUN apk add vim gcc g++ linux-headers libffi-dev
#
RUN pip install --upgrade pip
RUN pip install  -r requirements.txt