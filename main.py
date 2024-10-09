from fastapi import FastAPI, Request, HTTPException
from telegram_bot import send_telegram_notification
from air_quality import get_city_by_coords, get_city_by_ip, get_air_quality_data
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend

app = FastAPI()

# Инициализация кэша
FastAPICache.init(InMemoryBackend(), prefix="fastapi-cache")

@app.post("/get-city")
async def get_city(request: Request):
    geo_data = await request.json()

    if 'lat' in geo_data and 'lon' in geo_data:
        # Получаем город по геолокации
        city = get_city_by_coords(geo_data['lat'], geo_data['lon'])
    else:
        # Получаем IP клиента
        client_ip = request.client.host
        city = get_city_by_ip(client_ip)

        if not city:
            city = "Астрахань"  # Город по умолчанию

    return {"city": city}

@app.post("/subscribe")
async def subscribe(request: Request):
    data = await request.json()

    if 'telegram_id' not in data:
        raise HTTPException(status_code=400, detail="telegram_id required")

    city = data.get('city', "Астрахань")
    air_quality = get_air_quality_data(city)

    # Отправляем уведомление через Telegram
    await send_telegram_notification(data['telegram_id'], city, air_quality)

    return {"message": "Subscription successful"}
