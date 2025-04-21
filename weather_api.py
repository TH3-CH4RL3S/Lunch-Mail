import requests
import os
from dotenv import load_dotenv, find_dotenv
from smhi_symbols import describe_weather_code
from datetime import datetime, timezone
from dateutil import parser

load_dotenv(find_dotenv())
DEBUG = os.getenv("DEBUG", "false").lower() == "true"
EMAIL_SENDER = os.getenv("EMAIL_SENDER")

def get_coordinates(city_name):
    """Hämtar latitud och longitud från OpenStreetMap via Nominatim."""
    url = f"https://nominatim.openstreetmap.org/search"
    params = {
        "q": city_name,
        "format": "json",
        "limit": 1
    }
    headers = {
        "User-Agent": f"LunchBot {EMAIL_SENDER}" # Ange en användaragent för att undvika blockering av Nominatim
    }

    response = requests.get(url, params=params, headers=headers)
    response.raise_for_status()
    results = response.json()

    if not results:
        raise ValueError(f"Staden '{city_name}' hittades inte.")

    lat = round(float(results[0]["lat"]), 3)
    lon = round(float(results[0]["lon"]), 3)

    print(f"📍 {city_name} → lat: {lat}, lon: {lon}")
    return lat, lon

def get_weather_from_smhi(lat, lon):
    base_url = "https://opendata-download-metfcst.smhi.se/api/category/pmp3g/version/2"
    point_url = f"{base_url}/geotype/point/lon/{lon}/lat/{lat}/data.json"

    response = requests.get(point_url)
    response.raise_for_status()
    data = response.json()

    now = datetime.now(timezone.utc)

    # Hitta det närmaste tidssteget
    closest_step = min(
        data["timeSeries"],
        key=lambda step: abs(parser.isoparse(step["validTime"]) - now)
    )

    temperature = next(
        param["values"][0]
        for param in closest_step["parameters"]
        if param["name"] == "t"
    )

    weather_symbol = next(
        param["values"][0]
        for param in closest_step["parameters"]
        if param["name"] == "Wsymb2"
    )

    return temperature, weather_symbol, closest_step["validTime"]


# Hämta väder för vald stad
if DEBUG:
    city = "Karlskoga"
    lat, lon = get_coordinates(city)
    temp, wsymb_code, valid_time = get_weather_from_smhi(lat, lon)
    print(f"🌡️ {temp}°C vid {valid_time} (kod {wsymb_code})")
    description = describe_weather_code(wsymb_code)
    print(f"Väder: {description}")

