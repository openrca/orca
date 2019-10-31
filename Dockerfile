FROM python:3.7-alpine

MAINTAINER OpenRCA

WORKDIR /app

ADD ./requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt

COPY . /app

ENTRYPOINT ["python"]

CMD [ "manage.py", "run" ]