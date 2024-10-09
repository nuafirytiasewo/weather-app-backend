from fastapi import FastAPI, Request, HTTPException
from telegram_bot import send_telegram_notification
from air_quality import get_city_by_coords, get_city_by_ip, get_air_quality_data
from aiocache import cached

app = FastAPI()

@app.get("/api/get-city")
@cached(ttl=360000)  # Кэшируем результат на 1 час
async def get_city(request: Request):
    # geo_data = await request.json()

    # if 'lat' in geo_data and 'lon' in geo_data:
    #     city = get_city_by_coords(geo_data['lat'], geo_data['lon'])
    # else:
    #     client_ip = request.client.host
    #     city = get_city_by_ip(client_ip)

    #     if not city:
    #         city = "Астрахань"
    city = "Астрахань"
    return {"city": city}

@app.get("/api/subscribe")
async def subscribe(request: Request):
    data = await request.json()

    if 'telegram_id' not in data:
        raise HTTPException(status_code=400, detail="telegram_id required")

    city = data.get('city', "Астрахань")
    air_quality = get_air_quality_data(city)

    await send_telegram_notification(data['telegram_id'], city, air_quality)

    return {"message": "Subscription successful"}
