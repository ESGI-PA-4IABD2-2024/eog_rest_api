from typing import List, Dict
from db.mysql_requests import get_routes
from db.mysql_requests import get_platforms_data
from db.mysql_requests import get_overcrowded_platforms
from datetime import datetime
from datetime import timedelta


class Platform :
    def __init__(self
                 , id_platform: int
                 , minimal_arrival_time: float
                 , routes: List["Route"] = []
                 ):
        self.id_platform = id_platform
        self.minimal_arrival_time = minimal_arrival_time
        self.routes = routes
        self.parent: "Platform" = None
        self.line = None
        self.station_name = None
             
    
class Route:
    def __init__(self
                 , id_departure_platform: int
                 , id_arrival_platform: int
                 , departure_time: datetime
                 , arrival_time: datetime
                 , on_foot_travel_time: timedelta
                 ):
        self.id_departure_platform = id_departure_platform
        self.id_arrival_platform = id_arrival_platform
        if(on_foot_travel_time):
            self.is_on_foot: bool = True
            self.on_foot_travel_time = on_foot_travel_time
        else :
            self.is_on_foot: bool = False
            self.departure_time = departure_time
            self.arrival_time = arrival_time
        self.is_overcrowded = False


def get_optimal_route_from_departure(id_departure_platform: int
                                     , id_arrival_platform: int
                                     , departure_time: datetime
                                     , arrival_maximal_time: datetime
                                     , avoid_people: bool
                                     , on_foot_speed_multiplier: float
                                    ):
    
    def get_ancestry(current_platform: "Platform", is_a_change: bool):
        if (not current_platform.parent):
            return {"departure": f"{current_platform.station_name} - Ligne {current_platform.line}"}, 0, 0
        if (current_platform.id_platform == id_arrival_platform):
            current_route, number_of_elements, number_of_changes = get_ancestry(current_platform.parent, False)
            current_route[f"arrival"] = f"{current_platform.station_name} - Ligne {current_platform.line}"
        else:
            if (current_platform.parent.line != current_platform.line):
                current_route, number_of_elements, number_of_changes = get_ancestry(current_platform.parent, True)
                number_of_elements += 1
                number_of_changes += 1
                current_route[f"changement_{number_of_changes}"] = f"{current_platform.station_name} - Ligne {current_platform.line}"
            else:
                current_route, number_of_elements, number_of_changes = get_ancestry(current_platform.parent, False)
                number_of_elements += 1
                if is_a_change:
                    number_of_changes += 1
                    current_route[f"changement_{number_of_changes}"] = f"{current_platform.station_name} - Ligne {current_platform.line}"
                else:
                    current_route[f"node_{number_of_elements}"] = f"{current_platform.station_name} - Ligne {current_platform.line}"
        return current_route, number_of_elements, number_of_changes
    
    
    platforms: Dict[int, "Platform"] = {}
    db_routes: List[Dict] = get_routes(departure_time, arrival_maximal_time)
    for db_route in db_routes:
        route: "Route" = Route(db_route["id_departure_platform"]
                               , db_route["id_arrival_platform"]
                               , db_route["departure_time"]
                               , db_route["arrival_time"]
                               , db_route["on_foot_travel_time"])
        if route.id_departure_platform in platforms.keys():
            platforms[route.id_departure_platform].routes.append(route)
        else:
            platforms[route.id_departure_platform] = Platform(route.id_departure_platform
                                                            , 9999999999999999
                                                            , [route])
        route.id_departure_platform = platforms[route.id_departure_platform]
        
        if route.id_arrival_platform in platforms.keys():
            platforms[route.id_arrival_platform].routes.append(route)
        else:
            platforms[route.id_arrival_platform] = Platform(route.id_arrival_platform
                                                            , 9999999999999999
                                                            , [])
        route.id_arrival_platform = platforms[route.id_arrival_platform]
    overcrowded_platforms: List[int] = get_overcrowded_platforms()
    for platform_id in overcrowded_platforms:
        if platform_id in platforms.keys():
            platforms[platform_id].is_overcrowded = True
    
    if (platforms[id_departure_platform].is_overcrowded):
        return {"Error": "La station de départ est bondée ou fermée."}
    if (platforms[id_arrival_platform].is_overcrowded):    
        return {"Error": "La station d'arrivée est bondée ou fermée"}
    
    reached_arrival: bool = False
    unchecked_platforms: Dict["Platform"] = platforms.copy()
    platforms[id_departure_platform].minimal_arrival_time = departure_time
    current_platform: "Platform" = platforms[id_departure_platform]
    del unchecked_platforms[current_platform]
    took_off: bool = False
    
    while (not reached_arrival):
        for route in current_platform.routes :
            if (route.departure_time >= current_platform.minimal_arrival_time
                and route.id_arrival_platform in unchecked_platforms.keys()
                and not (avoid_people and unchecked_platforms[route.id_arrival_platform].is_overcrowded)
               ):
                if route.is_on_foot:
                    unchecked_platforms[route.id_arrival_platform].minimal_arrival_time = current_platform.minimal_arrival_time + (route.on_foot_travel_time * on_foot_speed_multiplier)
                else:
                    unchecked_platforms[route.id_arrival_platform].minimal_arrival_time = min(unchecked_platforms[route.id_arrival_platform].minimal_arrival_time, route.arrival_time)
                unchecked_platforms[route.id_arrival_platform].parent = current_platform
        
        current_platform = Platform(-1, 10000000000000000)
        for platform in unchecked_platforms.values():
            if platform.minimal_arrival_time < current_platform.minimal_arrival_time:
                current_platform = platform
        del unchecked_platforms[current_platform]
        if (current_platform.minimal_arrival_time == departure_time):
            id_departure_platform = current_platform.id_platform
        if current_platform == platforms[id_arrival_platform]:
            reached_arrival = True
        elif unchecked_platforms.is_empty():
            return {"Error": "Aucun trajet ne permet d'éviter les station bondées."}
    
    while (current_platform.parent.line != current_platform.line):
        current_platform = current_platform.parent
        id_arrival_platform = current_platform.id_platform
        
    platforms_in_optimal_route = set()
    platforms_in_optimal_route.add(id_arrival_platform)
    while (current_platform.id_platform != id_departure_platform and current_platform.parent):
        current_platform = current_platform.parent
        platforms_in_optimal_route.add(current_platform.id_platform)
    
    platforms_data: Dict = get_platforms_data(platforms_in_optimal_route)
    for platform_id, data in platforms_data.enumerate():
        platforms[platform_id].line = data["line"]
        platforms[platform_id].station_name = data["station_name"]
    
    return get_ancestry(platforms[id_arrival_platform], False)


def get_optimal_route_from_arrival(id_departure_platform: int
                                   , id_arrival_platform: int
                                   , departure_minimal_time: datetime
                                   , arrival_time: datetime
                                   , avoid_people: bool
                                   , on_foot_speed_multiplier: float
                                  ):
    return {"Error": "Comming soon"}
    

def get_optimal_route(id_departure_platform: int
                      , id_arrival_platform: int
                      , go_back_in_time: bool
                      , departure_minimal_time: float
                      , arrival_maximal_time: float
                      , avoid_people: bool
                      , on_foot_speed_multiplier: float
                     ):
    if id_departure_platform == id_arrival_platform:
        return {"Error": "Gares de départ et d'arrivée identiques."}
    if go_back_in_time :
        return get_optimal_route_from_arrival(id_departure_platform
                                              , id_arrival_platform
                                              , departure_minimal_time
                                              , arrival_maximal_time
                                              , avoid_people
                                              , on_foot_speed_multiplier)
    else:
        return get_optimal_route_from_departure(id_departure_platform
                                                , id_arrival_platform
                                                , departure_minimal_time
                                                , arrival_maximal_time
                                                , avoid_people
                                                , on_foot_speed_multiplier)



