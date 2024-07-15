from datetime import datetime
from datetime import timedelta

from .database_connection import get_db_connection


def get_routes(departure_time: datetime, arrival_time: datetime):
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
                      route_time IS NOT NULL \
                      OR departure_hour >= '{departure_time.strftime('%Y-%m-%d %H:%M:%S')}' \
                      AND arrival_hour <= '{arrival_time.strftime('%Y-%m-%d %H:%M:%S')}'"
        cursor.execute(query)
        routes_data = [
            {
                "id_departure_platform": row[0],
                "id_arrival_platform": row[1],
                "departure_time": row[2],
                "arrival_time": row[3],
                "on_foot_travel_time": timedelta(minutes=row[4]) if row[4] else None,
            }
            for row in cursor.fetchall()
        ]
        return routes_data

    except Exception as e:
        print(f"error: {e}")
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
        query = "SELECT \
                      id_platform \
                    , ligne_platform \
                    , name_cluster \
                  FROM \
                      platforms \
                      LEFT JOIN stations ON platforms.id_station = stations.id_gare \
                      LEFT JOIN cluster ON stations.id_cluster = cluster.id_cluster \
                  WHERE \
                      id_platform IN ({})".format(
            ",".join(["%s"] * len(platform_id_list))
        )
        cursor.execute(query, platform_id_list)
        platforms_data = {
            row[0]: {"line": row[1], "station_name": row[2]} for row in cursor.fetchall()
        }
        return platforms_data

    except Exception as e:
        print(f"error: {e}")
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
        query = "SELECT \
                      id_platform \
                  FROM \
                      malus \
                      INNER JOIN stations ON malus.id_cluster = stations.id_cluster \
                      INNER JOIN platforms ON stations.id_gare = platforms.id_station"
        cursor.execute(query)
        overcrowded_platforms = [row[0] for row in cursor.fetchall()]
        return overcrowded_platforms

    except Exception as e:
        print(f"error: {e}")
        return None

    finally:
        if connection:
            connection.close()


def get_first_platform_from_cluster(cluster_name: str):
    """
    Récupère un quai appartenant à cette gare/cluster.
    """
    connection = get_db_connection()
    if connection is None:
        return None

    try:
        cursor = connection.cursor(buffered=True)
        query = f"SELECT \
                      id_platform \
                  FROM \
                      cluster \
                      INNER JOIN stations ON cluster.id_cluster = stations.id_cluster \
                      INNER JOIN platforms ON stations.id_gare = platforms.id_station \
                  WHERE \
                      cluster.name_cluster = '{cluster_name}'"
        cursor.execute(query)
        platform = cursor.fetchone()[0]
        cursor.close()
        return platform

    except Exception as e:
        print(f"error: {e}")
        return None

    finally:
        if connection:
            connection.close()
