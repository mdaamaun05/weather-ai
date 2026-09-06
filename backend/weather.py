import requests


def get_weather(latitude, longitude):

    url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": latitude,
        "longitude": longitude,

        "hourly": [
            "temperature_2m",
            "relative_humidity_2m",
            "precipitation",
            "wind_speed_10m",
            "wind_gusts_10m",
            "cloud_cover",
            "pressure_msl",
            "vapour_pressure_deficit"
        ],

        "forecast_days": 2,
        "timezone": "auto"
    }

    response = requests.get(url, params=params)

    response.raise_for_status()

    return response.json()