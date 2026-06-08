FROM python:3.10-slim

WORKDIR /app

COPY requirements ./requirements

RUN pip install --upgrade pip

RUN pip install -r requirements/base.txt

COPY backend .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]