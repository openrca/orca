FROM python:3.7-alpine

MAINTAINER OpenRCA

WORKDIR /app

RUN apk update && \
    apk add --no-cache gcc musl-dev

ADD ./requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt

COPY . /app

CMD [ "honcho", "start" ]
