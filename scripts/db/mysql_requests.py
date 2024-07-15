from datetime import datetime
from datetime import timedelta

import pandas as pd

from .database_connection import get_db_connection


def get_routes(departure_time, arrival_time):
    """
    Récupère la liste des trajets.
    """
    connection = get_db_connection()
    if connection is None:
        return None

    try:
        cursor = connection.cursor()
        query = f"SELECT \
                      id_departure_platform \
                    , id_arrival_platform \
                    , departure_hour \
                    , arrival_hour \
                    , route_time \
                  FROM \
                      routes \
                  WHERE \
                      route_time NOT NULL
                      OR departure_hour >= {departure_time} and arrival_hour <= {arrival_time}"
        cursor.execute(query)
        routes_data = [{"id_departure_platform": row[0]
                        , "id_arrival_platform": row[1]
                        , "departure_time": row[2]
                        , "arrival_time": row[3]
                        , "on_foot_travel_time": timedelta(minutes = row[4]) if row[4] else None
                       } for row in cursor.fetchall()]
        return routes_data

    except Exception as e:
        print(f"Error: {e}")
        return None

    finally:
        if connection:
            connection.close()


def get_platforms_data(platform_id_list):
    """
    Récupère la ligne et le nom de la gare auxquelles appartient ce quai.
    """
    connection = get_db_connection()
    if connection is None:
        return None

    try:
        cursor = connection.cursor()
        query = f"SELECT \
                      id_platform \
                    , ligne_platform \
                    , name_cluster \
                  FROM \
                      PLATFORMS \
                      LEFT JOIN STATIONS ON PLATFORMS.id_station = STATIONS.id_gare \
                      LEFT JOIN CLUSTER ON STATIONS.id_cluster = CLUSTER.id_cluster \
                  WHERE \
                      id_platform IN ({platform_id_list})".format(",".join(["%s"] * len(platform_id_list)))
        cursor.execute(query, platform_id_list)
        platforms_data = {row[0]: {"line": row[1], "station_name": row[2]} for row in cursor.fetchall()}
        return platforms_data

    except Exception as e:
        print(f"Error: {e}")
        return None

    finally:
        if connection:
            connection.close()


def get_overcrowded_platforms():
    
    """
    Récupère l'ensemble des quais de gares bondées.
    """
    connection = get_db_connection()
    if connection is None:
        return None

    try:
        cursor = connection.cursor()
        query = f"SELECT \
                      id_platform \
                  FROM \
                      MALUS
                      INNER JOIN STATIONS ON MALUS.id_cluster = STATIONS.id_cluster \
                      INNER JOIN PLATFORMS ON STATIONS.id_station = PLATFORMS.id_gare"
        cursor.execute(query)
        overcrowded_platforms = [row[0] for row in cursor.fetchall()]
        return overcrowded_platforms

    except Exception as e:
        print(f"Error: {e}")
        return None

    finally:
        if connection:
            connection.close()
    
    