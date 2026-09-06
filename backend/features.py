import pandas as pd
import numpy as np


# Features that will be used by the ML model
FEATURE_COLUMNS = [
    "temperature",
    "humidity",
    "precipitation",
    "wind_speed",
    "wind_gust",
    "cloud_cover",
    "pressure",
    "vapour_pressure_deficit",
]


def weather_to_dataframe(weather_data):
    """
    Convert Open-Meteo JSON response into a Pandas DataFrame.
    """

    hourly = weather_data["hourly"]

    df = pd.DataFrame({
        "time": hourly["time"],
        "temperature": hourly["temperature_2m"],
        "humidity": hourly["relative_humidity_2m"],
        "precipitation": hourly["precipitation"],
        "wind_speed": hourly["wind_speed_10m"],
        "wind_gust": hourly["wind_gusts_10m"],
        "cloud_cover": hourly["cloud_cover"],
        "pressure": hourly["pressure_msl"],
        "vapour_pressure_deficit": hourly[
            "vapour_pressure_deficit"
        ],
    })

    return df


def create_features(weather_data):
    """
    Convert raw weather data into ML-ready features.
    """

    df = weather_to_dataframe(weather_data)

    # --------------------------------------------------
    # 1. Basic numerical features
    # --------------------------------------------------

    df["temperature"] = pd.to_numeric(
        df["temperature"],
        errors="coerce"
    )

    df["humidity"] = pd.to_numeric(
        df["humidity"],
        errors="coerce"
    )

    df["precipitation"] = pd.to_numeric(
        df["precipitation"],
        errors="coerce"
    )

    df["wind_speed"] = pd.to_numeric(
        df["wind_speed"],
        errors="coerce"
    )

    df["wind_gust"] = pd.to_numeric(
        df["wind_gust"],
        errors="coerce"
    )

    df["cloud_cover"] = pd.to_numeric(
        df["cloud_cover"],
        errors="coerce"
    )

    df["pressure"] = pd.to_numeric(
        df["pressure"],
        errors="coerce"
    )

    df["vapour_pressure_deficit"] = pd.to_numeric(
        df["vapour_pressure_deficit"],
        errors="coerce"
    )

    # --------------------------------------------------
    # 2. Time-based features
    # --------------------------------------------------

    df["time"] = pd.to_datetime(df["time"])

    df["hour"] = df["time"].dt.hour

    df["day"] = df["time"].dt.day

    df["month"] = df["time"].dt.month

    # --------------------------------------------------
    # 3. Rolling rainfall
    # --------------------------------------------------

    df["rain_3h"] = (
        df["precipitation"]
        .rolling(window=3, min_periods=1)
        .sum()
    )

    df["rain_6h"] = (
        df["precipitation"]
        .rolling(window=6, min_periods=1)
        .sum()
    )

    # --------------------------------------------------
    # 4. Wind change
    # --------------------------------------------------

    df["wind_change"] = (
        df["wind_speed"].diff()
    )

    # --------------------------------------------------
    # 5. Pressure change
    # --------------------------------------------------

    df["pressure_change"] = (
        df["pressure"].diff()
    )

    # --------------------------------------------------
    # 6. Humidity change
    # --------------------------------------------------

    df["humidity_change"] = (
        df["humidity"].diff()
    )

    # --------------------------------------------------
    # 7. Cloud change
    # --------------------------------------------------

    df["cloud_change"] = (
        df["cloud_cover"].diff()
    )

    # --------------------------------------------------
    # Replace missing values created by diff()
    # --------------------------------------------------

    df = df.replace(
        [np.inf, -np.inf],
        np.nan
    )

    df = df.ffill().bfill()

    return df


def get_model_features(weather_data):
    """
    Return only the features required by the ML model.
    """

    df = create_features(weather_data)

    model_features = [
        "temperature",
        "humidity",
        "precipitation",
        "wind_speed",
        "wind_gust",
        "cloud_cover",
        "pressure",
        "vapour_pressure_deficit",
        "rain_3h",
        "rain_6h",
        "wind_change",
        "pressure_change",
        "humidity_change",
        "cloud_change",
    ]

    return df[model_features]