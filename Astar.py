from typing import List, Dict

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
             
    
class Route:
    def __init__(self
                 , id_departure_platform: int
                 , id_arrival_platform: int
                 , departure_time: float
                 , arrival_time: float
                 , on_foot_travel_time: float
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


def get_route_from_departure(departure_platform: int
              , arrival_platform: int
              , departure_time: float
              , arrival_maximal_time: float
              , avoid_people: bool
              , on_foot_speed_multiplier: float
              ):
    platforms: Dict[int, "Platform"] = {}
    routes: List["Route"] = None #TODO get routes from DB
    for route in routes:
        newRoute: "Route" = route
        if route.id_departure_platform in platforms.keys():
            platforms[route.id_departure_platform].routes.append(newRoute)
        else:
            platforms[route.id_departure_platform] = Platform(route.id_departure_platform
                                                            , 9999999999999999
                                                            , [newRoute])
        newRoute.id_departure_platform = platforms[route.id_departure_platform]
        
        if route.id_arrival_platform in platforms.keys():
            platforms[route.id_arrival_platform].routes.append(newRoute)
        else:
            platforms[route.id_arrival_platform] = Platform(route.id_arrival_platform
                                                            , 9999999999999999
                                                            , [])
        newRoute.id_arrival_platform = platforms[route.id_arrival_platform]
    overcrowded_platforms: List[int] = None #TODO get overcrowded platforms of that date 
    for platform_id in overcrowded_platforms:
        if platform_id in platforms.keys():
            platforms[platform_id].is_overcrowded = True
    
    if (platforms[departure_platform].is_overcrowded):
        raise Exception #TODO
    if (platforms[arrival_platform].is_overcrowded):    
        raise Exception #TODO
    
    reached_arrival: bool = False
    unchecked_platforms: Dict["Platform"] = platforms.copy()
    platforms[departure_platform].minimal_arrival_time = departure_time
    current_platform: "Platform" = platforms[departure_platform]
    del unchecked_platforms[current_platform]
    
    while (not reached_arrival):
        
        for route in current_platform.routes :
            if route.departure_time >= current_platform.minimal_arrival_time \
               and route.id_arrival_platform in unchecked_platforms.keys() \
               and not (avoid_people and unchecked_platforms[route.id_arrival_platform].is_overcrowded):
                if route.is_on_foot:
                    unchecked_platforms[route.id_arrival_platform].minimal_arrival_time = current_platform.minimal_arrival_time + (route.on_foot_travel_time * on_foot_speed_multiplier)
                else:
                    unchecked_platforms[route.id_arrival_platform].minimal_arrival_time = min(unchecked_platforms[route.id_arrival_platform].minimal_arrival_time, route.arrival_time)
        
        current_platform = Platform(-1, 10000000000000000)
        for platform in unchecked_platforms.values():
            if platform.minimal_arrival_time < current_platform.minimal_arrival_time:
                current_platform = platform
        del unchecked_platforms[current_platform]
        if current_platform == platforms[arrival_platform]:
            reached_arrival = True
        elif unchecked_platforms.is_empty():
            raise Exception #TODO + depends if wants to avoid crowds


def get_route_from_arrival(departure_platform: int
              , arrival_platform: int
              , departure_minimal_time: float
              , arrival_time: float
              , avoid_people: bool
              , on_foot_speed_multiplier: float
              ):
    pass
    

def get_route(departure_platform: int
              , arrival_platform: int
              , go_back_in_time: bool
              , departure_minimal_time: float
              , arrival_maximal_time: float
              , avoid_people: bool
              , on_foot_speed_multiplier: float
              ):
    if departure_platform == arrival_platform:
        raise Exception #TODO
    if go_back_in_time :
        get_route_from_arrival(departure_platform
                               , arrival_platform
                               , departure_minimal_time
                               , arrival_maximal_time
                               , avoid_people
                               , on_foot_speed_multiplier)
    else:
        get_route_from_departure(departure_platform
                               , arrival_platform
                               , departure_minimal_time
                               , arrival_maximal_time
                               , avoid_people
                               , on_foot_speed_multiplier)



