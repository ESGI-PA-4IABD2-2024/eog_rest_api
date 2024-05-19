FROM python:3.11-slim
LABEL author="AntoineTSIO"

WORKDIR /app

RUN apt-get update && \
    apt-get install -y default-libmysqlclient-dev gcc git && \
    pip install --upgrade pip && \
    pip install \
        mysql-connector-python \
        python-dotenv \
        fastapi \
        uvicorn

COPY . .

CMD ["python", "api.py"]
