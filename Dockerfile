FROM debian:latest

WORKDIR /app

COPY . .

RUN apt-get update -y && \
    apt-get install -y \
    python3 \
    python3-pip \
    python3-venv

RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

RUN pip install --no-cache-dir \
    fastapi \
    uvicorn \
    mysql-connector-python \
    python-dotenv

CMD ["python3", "api.py"]
