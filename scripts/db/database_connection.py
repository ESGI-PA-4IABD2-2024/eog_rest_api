import os

import mysql.connector
from dotenv import load_dotenv

load_dotenv()


def get_db_connection():
    global db_connection
    try:
        db_connection = mysql.connector.connect(
            host=os.environ.get("DATABASE_ADDRESS"),
            user=os.environ.get("DATABASE_USERNAME"),
            password=os.environ.get("DATABASE_PASSWORD"),
            port=os.environ.get("DATABASE_PORT"),
            database=os.environ.get("DATABASE_NAME"),
        )
        return db_connection
    except Exception as e:
        print(f"Error: {e}")
        return None
