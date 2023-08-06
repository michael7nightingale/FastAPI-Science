FROM python:3.11

COPY requirements.txt ./requirements.txt
COPY src ./app
COPY .docker.env ./.docker.env
COPY alembic.ini ./alembic.ini

RUN pip install -r /requirements.txt

EXPOSE 8000

