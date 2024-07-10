import os

import mysql.connector
from dotenv import load_dotenv

load_dotenv()
db_connection = None


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


def get_open_stations():
    connection = get_db_connection()
    if connection is None:
        return None
    try:
        cursor = connection.cursor()
        query = "SELECT DISTINCT nom FROM stations_app WHERE ouverte=1 ORDER BY nom"
        cursor.execute(query)
        stations_list = cursor.fetchall()

        stations = []
        for station in stations_list:
            stations.append({"nom": station[0]})

        cursor.close()
        return stations
    except Exception as e:
        print(f"Error: {e}")
        return None
    finally:
        if connection:
            connection.close()
