import requests
from dotenv import load_dotenv
import os

load_dotenv()

OPENWEATHER_API_KEY = os.getenv('OPENWEATHER_API_KEY')

def get_city_by_coords(lat, lon):
    url = f"https://api.openweathermap.org/geo/1.0/reverse?lat={lat}&lon={lon}&appid={OPENWEATHER_API_KEY}"
    response = requests.get(url)
    data = response.json()
    if data:
        return data[0]["name"]
    return None

def get_city_by_ip(ip):
    url = f"https://ipinfo.io/{ip}/geo"
    response = requests.get(url)
    data = response.json()
    if "city" in data:
        return data["city"]
    return None

def get_air_quality_data(city):
    # Пример получения данных о загрязнении воздуха
    url = f"http://api.openweathermap.org/data/2.5/air_pollution?q={city}&appid={OPENWEATHER_API_KEY}"
    response = requests.get(url)
    data = response.json()
    if "list" in data:
        return data["list"][0]["main"]["aqi"]
    return "Неизвестно"
