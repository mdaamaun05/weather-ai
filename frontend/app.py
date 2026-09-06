import streamlit as st
import requests
import pandas as pd
import plotly.express as px


st.set_page_config(
    page_title="AI Weather Warning",
    page_icon="🌦️",
    layout="wide"
)


st.title("🌦️ AI-Driven Hyper-Local Weather Warning")

st.sidebar.header("Location")

latitude = st.sidebar.number_input(
    "Latitude",
    value=17.3850
)

longitude = st.sidebar.number_input(
    "Longitude",
    value=78.4867
)


if st.sidebar.button("Get Weather"):

    response = requests.get(
        "http://127.0.0.1:8000/weather",
        params={
            "latitude": latitude,
            "longitude": longitude
        }
    )

    data = response.json()

    hourly = data["hourly"]

    df = pd.DataFrame(hourly)

    st.subheader("Current Weather Data")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Temperature",
        f"{df['temperature_2m'].iloc[0]} °C"
    )

    col2.metric(
        "Humidity",
        f"{df['relative_humidity_2m'].iloc[0]} %"
    )

    col3.metric(
        "Rain",
        f"{df['precipitation'].iloc[0]} mm"
    )

    col4.metric(
        "Wind",
        f"{df['wind_speed_10m'].iloc[0]} km/h"
    )


    st.subheader("Temperature Forecast")

    fig = px.line(
        df,
        x="time",
        y="temperature_2m",
        title="Temperature"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


    st.subheader("Rainfall Forecast")

    fig = px.bar(
        df,
        x="time",
        y="precipitation",
        title="Precipitation"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )