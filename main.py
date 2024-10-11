from fastapi import FastAPI, Request, Query
from telegram_bot import send_telegram_notification
from air_quality import get_city_by_coords, get_city_by_ip, get_air_pollution_data, get_air_pollution_forecast
from aiocache import cached
from fastapi.middleware.cors import CORSMiddleware

from app.bot.telegram_bot import on_startup
from scheduler import start_scheduler

app = FastAPI()

# Разрешаем CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Разрешаем фронтенд адресу делать запросы
    allow_credentials=True,
    allow_methods=["*"],  # Разрешаем все методы (GET, POST, и т.д.)
    allow_headers=["*"],  # Разрешаем все заголовки
)

#получить город
@app.get("/api/get-city")  # Оставляем как GET
@cached(ttl=360000)  # Кэшируем результат на 1 час
async def get_city(lat: float = None, lon: float = None, request: Request = None):
    if lat is not None and lon is not None:
        # Получаем город по координатам
        city = await get_city_by_coords(lat, lon)
    else:
        # Получаем город по IP
        client_ip = request.client.host
        city, lat, lon = get_city_by_ip(client_ip)
        
        if not city:
            city = "Астрахань"
            lat = "46.377687" 
            lon = "48.053186"

    # Возвращаем название города и координаты
    return {
        "city": city,
        "coordinates": {
            "lat": lat,
            "lon": lon
        }
    }

#получить текущее качество воздуха
@app.get("/api/get-pollution")
async def get_pollution(lat: float, lon: float):
    data = await get_air_pollution_data(lat, lon)
    return data

#получить прогноз качества воздуха на 5 дней
@app.get("/api/get-forecast")
async def get_forecast(lat: float, lon: float):
    data = await get_air_pollution_forecast(lat, lon)
    return data

#отправить сообщение по 
@app.get("/api/subscribe")
async def subscribe(
    telegram_id: str = Query(...),
    city: str = Query(...),
    coordinates: str = Query(...)
):
    
    # air_quality = get_air_quality_data(city)
    await send_telegram_notification(telegram_id, city, coordinates)

    return {"message": "Subscription successful"}

@app.on_event("startup")
async def startup_event():
    await on_startup()
    start_scheduler()

@app.get("/api/geo")
async def get_geo():
    return {"lon": 12.34, "lat": 56.78}  # Пример, здесь должно быть получение реальных данных

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)