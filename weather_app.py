import streamlit as st
import requests
import datetime
import pandas as pd
import plotly.express as px

# --- API Keys ---
WEATHER_API_KEY = "88fd7f086ca73f36a837dca76c634adb"

# --- URLs ---
WEATHER_URL = "http://api.openweathermap.org/data/2.5/weather"
FORECAST_URL = "http://api.openweathermap.org/data/2.5/forecast"
IPINFO_URL = "http://ip-api.com/json/"

# --- Theme Control ---
if "theme" not in st.session_state:
    st.session_state.theme = "Dark"

# Sidebar Theme Toggle
with st.sidebar:
    st.markdown("### ⚙️ Settings")
    theme_option = st.radio("🌓 Select Theme", options=["Light", "Dark"], index=0 if st.session_state.theme == "Light" else 1)
    if theme_option != st.session_state.theme:
        st.session_state.theme = theme_option
        st.rerun()  # <== use this instead of experimental_rerun
    use_location = st.checkbox("📍 Auto-detect my city", value=False)

# --- Theme colors ---
def get_color_style():
    return {
        "header": "#1e90ff" if st.session_state.theme == "Light" else "#00f2ff",
        "text": "#000000" if st.session_state.theme == "Light" else "#FFFFFF",
    }

colors = get_color_style()

# --- Functions ---
def get_weather(city):
    return requests.get(WEATHER_URL, params={"q": city, "appid": WEATHER_API_KEY, "units": "metric"}).json()

def get_forecast(city):
    return requests.get(FORECAST_URL, params={"q": city, "appid": WEATHER_API_KEY, "units": "metric"}).json()

def alert_conditions(temp, wind, desc):
    alerts = []
    if temp > 38: alerts.append("🔥 Heat Alert")
    if temp < 5: alerts.append("❄️ Cold Alert")
    if wind > 10: alerts.append("🌪️ High Wind")
    if any(x in desc.lower() for x in ["storm", "thunder", "snow"]):
        alerts.append("⚡ Severe Weather")
    return alerts

def get_user_location():
    res = requests.get(IPINFO_URL)
    return res.json().get("city", "")

def get_uv_index(lat, lon):
    url = "https://api.openweathermap.org/data/2.5/onecall"
    params = {"lat": lat, "lon": lon, "exclude": "minutely,hourly,daily,alerts", "appid": WEATHER_API_KEY, "units": "metric"}
    res = requests.get(url, params=params)
    return res.json().get("current", {}).get("uvi", None)

def get_air_quality(lat, lon):
    url = "http://api.openweathermap.org/data/2.5/air_pollution"
    params = {"lat": lat, "lon": lon, "appid": WEATHER_API_KEY}
    res = requests.get(url, params=params)
    data = res.json()
    if data and data.get("list"):
        return data["list"][0]["main"]["aqi"]
    return None

def clothing_advice(temp, desc):
    if "rain" in desc or "storm" in desc:
        return "☔ Carry an umbrella or raincoat!"
    if temp > 30:
        return "🍛 Light clothes, stay hydrated."
    elif temp > 20:
        return "👕 T-shirt weather, maybe a light jacket."
    elif temp > 10:
        return "🧥 Wear a jacket or hoodie."
    else:
        return "🧣 Dress warmly with layers!"

# --- App Start ---
st.set_page_config("🌤️ Weather Pro App", layout="wide")

# --- Header ---
st.markdown(f"<h1 style='color:{colors['header']};'>🌤️ Real-Time Weather Pro</h1>", unsafe_allow_html=True)

city = get_user_location() if use_location else st.text_input("🔍 Enter City Name")

if city and st.button("Get Weather"):
    weather = get_weather(city)
    forecast = get_forecast(city)

    if weather.get("cod") != 200:
        st.error("City not found.")
    else:
        st.markdown(f"### 📍 {city.capitalize()} — {weather['weather'][0]['description'].capitalize()}")
        st.image(f"http://openweathermap.org/img/wn/{weather['weather'][0]['icon']}@2x.png", width=100)

        col1, col2, col3 = st.columns(3)
        col1.metric("🌡️ Temp", f"{weather['main']['temp']}\u00b0C")
        col2.metric("💨 Wind", f"{weather['wind']['speed']} m/s")
        col3.metric("💧 Humidity", f"{weather['main']['humidity']}%")

        alerts = alert_conditions(weather['main']['temp'], weather['wind']['speed'], weather['weather'][0]['description'])
        if alerts:
            st.warning(" | ".join(alerts))

        lat = weather["coord"]["lat"]
        lon = weather["coord"]["lon"]

        uvi = get_uv_index(lat, lon)
        if uvi is not None:
            st.markdown(f"#### 🌞 UV Index: `{uvi}`")
            if uvi <= 2:
                st.success("Low - Safe to be outside.")
            elif uvi <= 5:
                st.warning("Moderate - Wear sunglasses and sunscreen.")
            else:
                st.error("High - Avoid midday sun, use protection!")

        aqi = get_air_quality(lat, lon)
        aqi_level = {1: "Good", 2: "Fair", 3: "Moderate", 4: "Poor", 5: "Very Poor"}
        if aqi:
            st.markdown(f"#### 🪱 AQI: `{aqi}` — **{aqi_level[aqi]}**")

        st.info(f"👕 Clothing Advice: {clothing_advice(weather['main']['temp'], weather['weather'][0]['description'])}")

        # Forecast Chart
        st.markdown("### 📊 5-Day Forecast")
        forecast_df = pd.DataFrame([
            {"DateTime": entry["dt_txt"], "Temperature (°C)": entry["main"]["temp"]}
            for entry in forecast["list"]
        ])
        fig = px.line(forecast_df, x="DateTime", y="Temperature (°C)", title="Temperature Trend", markers=True)
        fig.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)

        # Forecast Summary
        st.markdown("### 🗕️ Daily Summary")
        seen_dates = set()
        for item in forecast["list"]:
            date = item["dt_txt"].split()[0]
            if date not in seen_dates:
                seen_dates.add(date)
                with st.expander(f"🗖️ {date}"):
                    icon = item["weather"][0]["icon"]
                    desc = item["weather"][0]["description"].capitalize()
                    temp = item["main"]["temp"]
                    wind = item["wind"]["speed"]
                    humidity = item["main"]["humidity"]
                    st.image(f"http://openweathermap.org/img/wn/{icon}.png", width=60)
                    st.write(f"**Description:** {desc}")
                    st.write(f"**Temp:** {temp}°C")
                    st.write(f"**Wind:** {wind} m/s")
                    st.write(f"**Humidity:** {humidity}%")
