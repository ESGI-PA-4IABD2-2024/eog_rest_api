import uvicorn
from fastapi import FastAPI
from fastapi import Response
from fastapi.middleware.cors import CORSMiddleware

from db_interactions import get_open_stations

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
    departure_to_arrival = {
        "departure": departure_location,
        "node_1": "node_1",
        "node_2": "node_2",
        "node_3": "node_3",
        "node_4": "node_4",
        "node_5": "node_5",
        "node_6": "node_6",
        "node_7": "node_7",
        "changement_1": "node_8",
        "changement_2": "node_9",
        "node_10": "node_10",
        "node_11": "node_11",
        "node_12": "node_12",
        "node_13": "node_13",
        "node_14": "node_14",
        "node_15": "node_15",
        "node_16": "node_16",
        "changement_3": "node_17",
        "changement_4": "node_18",
        "node_19": "node_19",
        "node_20": "node_20",
        "node_21": "node_21",
        "arrival": arrival_location,
    }
    response.headers["Content-Type"] = "application/json; charset=utf-8"
    return departure_to_arrival


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
