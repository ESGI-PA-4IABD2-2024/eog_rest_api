FROM python:3.11-slim-buster

RUN apt-get update && apt-get install -y \
    python3-fastapi \
    python3-uvicorn \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir mysql-connector-python python-dotenv

CMD ["python", "api.py"]
