from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.db.database import SessionLocal
from aiogram import Bot
import requests

from dotenv import load_dotenv
import os

load_dotenv()

API_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
bot = Bot(token=API_TOKEN)

async def send_notifications():
    async with SessionLocal() as session:
        result = await session.execute("SELECT * FROM subscriptions")
        subs = result.fetchall()

        for sub in subs:
            # Получаем данные о воздухе по координатам через API
            url = f"https://api.openweathermap.org/data/2.5/air_pollution?lat={sub.lat}&lon={sub.lon}&appid=YOUR_API_KEY"
            response = requests.get(url).json()
            aqi = response['list'][0]['main']['aqi']

            if aqi > 2:  # Например, AQI выше 2 = плохое качество
                await bot.send_message(sub.user_id, f"⚠️ Качество воздуха в {sub.city} ухудшилось!")

scheduler = AsyncIOScheduler()
scheduler.add_job(send_notifications, "interval", minutes=30)

def start_scheduler():
    scheduler.start()
