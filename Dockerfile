FROM python:3.9-slim
LABEL author="AntoineTSIO"

WORKDIR /app

RUN apt-get update && \
    apt-get install -y default-libmysqlclient-dev gcc git && \
    pip install --upgrade pip && \
    pip install \
        mysql-connector-python \
        fastapi \
        uvicorn \
        python-dotenv \
        git+https://github.com/Rapptz/discord.py@cb3ea9b889dcdefa5aa81b1dc7ce4e3e87abeeb0

COPY . .

CMD ["python", "api.py"]
