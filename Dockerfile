FROM debian:latest
LABEL author="AntoineTSIO"

WORKDIR /app

RUN apt-get update -y
RUN apt-get install -y \
  python3-fastapi \
  python3-uvicorn \
  python3-mysql-connector-python \
  python3-python-dotenv

RUN apt-get update

COPY . .

CMD ["python", "api.py"]
