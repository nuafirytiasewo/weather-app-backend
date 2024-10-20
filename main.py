from fastapi import FastAPI, Request, Query
from app.bot.telegram_bot import start_bot, send_notifications
from air_quality import get_city_by_coords, get_city_by_ip, get_air_pollution_data, get_air_pollution_forecast
from aiocache import cached
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import uvicorn

app = FastAPI()

# Разрешаем CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Разрешаем фронтенд адресу делать запросы
    allow_credentials=True,
    allow_methods=["*"],  # Разрешаем все методы (GET, POST и т.д.)
    allow_headers=["*"],  # Разрешаем все заголовки
)

# Получить город
@app.get("/api/get-city")
async def get_city(lat: float = None, lon: float = None, request: Request = None):
    if lat is not None and lon is not None:
        city = await get_city_by_coords(lat, lon)
    else:
        client_ip = request.client.host
        city, lat, lon = get_city_by_ip(client_ip)
        
        if not city:
            city = "Астрахань"
            lat = "46.377687" 
            lon = "48.053186"

    return {
        "city": city,
        "coordinates": {
            "lat": lat,
            "lon": lon
        }
    }

# Получить текущее качество воздуха
@app.get("/api/get-pollution")
async def get_pollution(lat: float, lon: float):
    data = await get_air_pollution_data(lat, lon)
    return data

# Получить прогноз качества воздуха на 5 дней
@app.get("/api/get-forecast")
async def get_forecast(lat: float, lon: float):
    data = await get_air_pollution_forecast(lat, lon)
    return data

# запускает бота
@app.on_event("startup")
async def startup_event():
    # Запуск бота
    asyncio.create_task(start_bot())
    # Запускаем функцию отправки уведомлений
    asyncio.create_task(send_notifications())

@app.get("/api/geo")
async def get_geo():
    return {"lon": 12.34, "lat": 56.78}  # Пример, здесь должно быть получение реальных данных

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
