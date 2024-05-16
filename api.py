import uvicorn
from fastapi import FastAPI
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
def departure_arrival(departure_location: str, arrival_location: str):
    print(f"Departure: {departure_location}")
    print(f"Arrival: {arrival_location}")
    return {"Departure": departure_location, "Arrival": arrival_location}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
