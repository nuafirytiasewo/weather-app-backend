from fastapi import FastAPI, Request, HTTPException, Query
from telegram_bot import send_telegram_notification
from air_quality import get_city_by_coords, get_city_by_ip, get_air_quality_data
from aiocache import cached

app = FastAPI()

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

@app.get("/api/subscribe")
async def subscribe(
    telegram_id: str = Query(...),
    city: str = Query(...),
    coordinates: str = Query(...)
):
    # Ваш код для обработки подписки
    # air_quality = get_air_quality_data(city)
    await send_telegram_notification(telegram_id, city, coordinates)

    return {"message": "Subscription successful"}
