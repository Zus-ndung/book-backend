FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 8000

HEALTHCHECK CMD curl --fail http://localhost:8000/health

CMD ["uvicorn", "--host", "0.0.0.0", "--port", "8000", "main:app"]