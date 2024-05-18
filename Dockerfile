FROM python:3.11-slim

RUN apt-get update

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir mysql-connector-python python-dotenv fastapi uvicorn

CMD ["python", "api.py"]
