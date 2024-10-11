from aiogram import Bot, Dispatcher, types
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import Command
from aiogram.types import Message
from aiogram import F

import asyncio
import logging

from dotenv import load_dotenv
import os

load_dotenv()

API_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

# Логирование
logging.basicConfig(level=logging.INFO)

# Создание экземпляра бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# Хэндлер команды /start с параметрами
@dp.message(Command("start"))
async def start(message: Message):
    # Пример получения параметров из deeplink
    if message.text and "start=" in message.text:
        params = message.text.split("start=")[-1].split("&")
        lon = params[0].split("=")[-1]
        lat = params[1].split("=")[-1]
        city = params[2].split("=")[-1]

        # Сохранение данных в базу (здесь должен быть код сохранения в БД)
        # Например, сохранение user_id, lon, lat и city

        await message.answer(f"Спасибо за подписку на рассылку!\nГород: {city}\nКоординаты: {lon}, {lat}")

# Функция отправки уведомлений
async def send_notification():
    # Логика пробежки по базе данных и проверки условий загрязнения
    # Например, каждый полчаса отправляем уведомления
    while True:
        # Пример: отправляем уведомление пользователям
        users = []  # Здесь должна быть выборка пользователей из БД
        for user in users:
            user_id = user["user_id"]
            city = user["city"]
            # Пример проверки качества воздуха (в реальном проекте заменить реальными данными)
            await bot.send_message(user_id, f"Внимание! В городе {city} превышен уровень загрязнений!")
        
        # Ожидаем 30 минут перед следующей проверкой
        await asyncio.sleep(1800)

# Хэндлер для остановки уведомлений
@dp.message(Command("stop"))
async def stop_notification(message: Message):
    # Логика удаления записи пользователя из базы
    user_id = message.from_user.id
    # Пример удаления данных пользователя из БД
    await message.answer("Вы отписались от рассылки уведомлений.")

# Запуск бота
async def main():
    dp.include_router(dp.router)

    # Запуск функции отправки уведомлений в фоне
    asyncio.create_task(send_notification())

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

# Функция on_startup для импорта в main.py
async def on_startup():
    logging.info("Бот запущен и готов к работе!")

