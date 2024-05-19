FROM arm64v8/python:3.11-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir mysql-connector-python python-dotenv fastapi uvicorn

CMD ["python", "api.py"]
