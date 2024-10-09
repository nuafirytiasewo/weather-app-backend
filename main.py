from fastapi import FastAPI, Request, HTTPException
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

@app.post("/api/subscribe")
async def subscribe(request: Request):
    data = await request.json()

    if 'telegram_id' not in data:
        raise HTTPException(status_code=400, detail="telegram_id required")

    city = data.get('city', "Астрахань")
    air_quality = get_air_quality_data(city)

    await send_telegram_notification(data['telegram_id'], city, air_quality)

    return {"message": "Subscription successful"}
