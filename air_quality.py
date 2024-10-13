import requests
from dotenv import load_dotenv
import os

load_dotenv()

OPENWEATHER_API_KEY = os.getenv('OPENWEATHER_API_KEY')

#получаем город по координатам с API
async def get_city_by_coords(lat, lon):
    url = f"https://api.openweathermap.org/geo/1.0/reverse?lat={lat}&lon={lon}&appid={OPENWEATHER_API_KEY}"
    response = requests.get(url)
    data = response.json()
    if data:
        return data[0]["name"]
    return None

#получаем город по ip
def get_city_by_ip(ip):
    if ":" in ip:
        ip = ip[:ip.index(":")]

    print(ip)
    url = f"https://ipinfo.io/{ip}/geo"
    response = requests.get(url)
    data = response.json()
    
    # Проверяем, есть ли поле city
    if "city" in data:
        city = data["city"]
    else:
        city = None

    # Проверяем, есть ли поле loc
    loc = data.get("loc")
    if loc:
        # Разделяем координаты на широту и долготу
        lat, lon = map(float, loc.split(","))
    else:
        lat, lon = None, None

    return city, lat, lon

#получаем текущие данные о качестве воздуха с API
async def get_air_pollution_data(lat, lon):
    url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={OPENWEATHER_API_KEY}"
    response = requests.get(url)
    return response.json()

#получаем прогноз качества воздуха на пять дней с API
async def get_air_pollution_forecast(lat, lon):
    url = f"http://api.openweathermap.org/data/2.5/air_pollution/forecast?lat={lat}&lon={lon}&appid={OPENWEATHER_API_KEY}"
    response = requests.get(url)
    return response.json()
