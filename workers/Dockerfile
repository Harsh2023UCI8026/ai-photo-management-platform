FROM python:3.10-slim

WORKDIR /app

COPY requirements ./requirements

RUN pip install --upgrade pip

RUN pip install -r requirements/base.txt

COPY workers .

CMD ["celery", "-A", "celery_app", "worker", "--loglevel=info"]