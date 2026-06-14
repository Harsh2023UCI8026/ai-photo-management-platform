FROM python:3.10-slim

WORKDIR /app


RUN apt-get update && apt-get install -y \
tesseract-ocr \
&& rm -rf /var/lib/apt/lists/*

COPY requirements ./requirements

RUN pip install --upgrade pip
RUN pip install -r requirements/base.txt

RUN pip install \
torch \
--index-url https://download.pytorch.org/whl/cpu

RUN pip install -r requirements/ai.txt

# backend code
COPY backend .

# ai services
COPY ai_services ./ai_services

# alembic config
COPY alembic.ini .

# migrations
COPY database ./database

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]