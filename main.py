from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.weather import get_weather

app = FastAPI(
    title="AI Weather Early Warning API"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():

    return {
        "message": "AI Weather Early Warning System"
    }


@app.get("/weather")
def weather(
    latitude: float,
    longitude: float
):

    data = get_weather(
        latitude,
        longitude
    )

    return data