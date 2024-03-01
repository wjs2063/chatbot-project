FROM python:3.11.5-alpine

MAINTAINER jaehyeonJeon


COPY . /code/
WORKDIR /code/backend/server

RUN apk add vim gcc g++ linux-headers libffi-dev
#
RUN pip install --upgrade pip
RUN pip install  -r requirements.txt

WORKDIR /code/backend/server/app

ENTRYPOINT ["uvicorn", "main:app","--host","0.0.0.0","--port","8000"]
