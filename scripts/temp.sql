SELECT \
    id_departure_platform \
  , id_arrival_platform \
  , departure_hour \
  , arrival_hour \
  , route_time \
FROM \
    routes \
WHERE \
    route_time NOT NULL
    OR departure_hour >= {} and arrival_hour <= {}