from datetime import datetime
from datetime import timedelta

import uvicorn
from fastapi import FastAPI
from fastapi import Response
from fastapi.middleware.cors import CORSMiddleware

from db_interactions import get_open_stations
from scripts.Astar import get_optimal_route

app = FastAPI()

origins = ["http://localhost"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/request/stations")
def request_stations():
    stations = get_open_stations()
    return {"stations": stations}


@app.get("/departure-arrival/{departure_location}/{arrival_location}")
def departure_arrival(departure_location: str, arrival_location: str, response: Response):
    print(f"Departure: {departure_location}")
    print(f"Arrival: {arrival_location}")
    departure_time = datetime.now()
    arrival_time = departure_time + timedelta(hours=2)
    departure_to_arrival = get_optimal_route(
        departure_location,
        arrival_location,
        go_back_in_time=False,
        departure_minimal_time=departure_time,
        arrival_maximal_time=arrival_time,
        avoid_people=True,
        on_foot_speed_multiplier=1,
    )
    print(departure_to_arrival)
    response.headers["Content-Type"] = "application/json; charset=utf-8"
    return departure_to_arrival


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
