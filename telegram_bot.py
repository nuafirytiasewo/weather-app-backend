import requests
from dotenv import load_dotenv
import os

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv('YOUR_TELEGRAM_BOT_TOKEN')

def send_message(telegram_id, message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': telegram_id,
        'text': message
    }
    requests.post(url, json=payload)

async def send_telegram_notification(telegram_id, city, air_quality):
    message = f"Уведомление! В городе {city} уровень загрязнения воздуха: {air_quality}."
    send_message(telegram_id, message)
