FROM python:3.11.5-alpine

MAINTAINER jaehyeonJeon


COPY . /code/
WORKDIR /code/backend/server

RUN apk add vim gcc g++ linux-headers libffi-dev
#
RUN pip install --upgrade pip
RUN pip install gunicorn
RUN pip install  -r requirements.txt

WORKDIR /code
#gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:80
ENTRYPOINT ["gunicorn","-c","gunicorn_conf.py"]
