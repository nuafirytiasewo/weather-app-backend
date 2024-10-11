from aiogram import Bot, Dispatcher, types
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import Command
from aiogram.types import Message
import asyncio
import logging
from dotenv import load_dotenv
import os
from geopy.geocoders import Nominatim

load_dotenv()

API_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

# Логирование
logging.basicConfig(level=logging.INFO)

# Создание экземпляра бота
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()

# Создание диспетчера
dp = Dispatcher(storage=storage)  # Передаем storage в диспетчер

# Хэндлер команды /start с параметрами
@dp.message(Command("start"))
async def start(message: Message):
    logging.info(f"Получена команда /start от {message.from_user.id}")
    logging.info(f"А что именно передалось {message.text}")
    
    # Проверяем, что текст команды содержит необходимые параметры
    if message.text and "lon" in message.text and "lat" in message.text:
        # Извлекаем координаты с помощью регулярных выражений
        lon = message.text.split("lon")[1].split("lat")[0]  # Извлечение долготы
        lat = message.text.split("lat")[1]  # Извлечение широты

        # Удаляем возможные лишние символы, такие как "-" перед значением
        lon = lon.replace("-", ".")  # Заменяем "-" на "." для долготы
        lat = lat.replace("-", ".")  # Заменяем "-" на "." для широты

        # Используем geocoder для определения города
        geolocator = Nominatim(user_agent="geoapiExercises")
        location = geolocator.reverse(f"{lat}, {lon}")
        city = location.raw['address'].get('city', 'Неизвестно')

        # Здесь должен быть код сохранения в БД

        await message.answer(f"Спасибо за подписку на рассылку!\nГород: {city}\nКоординаты: {lon}, {lat}")
    else:
        await message.answer("Пожалуйста, укажите координаты в формате: /start lon36-19lat51-73")

# Функция отправки уведомлений
async def send_notification():
    # Логика пробежки по базе данных и проверки условий загрязнения
    # Например, каждый полчаса отправляем уведомления
    while True:
        # Здесь должна быть выборка пользователей из БД
        users = []  # Пример пустого списка, замените на вашу выборку
        
        for user in users:
            user_id = user["user_id"]
            city = user["city"]
            # Пример проверки качества воздуха
            await bot.send_message(user_id, f"Внимание! В городе {city} превышен уровень загрязнений!")
        
        await asyncio.sleep(1800)  # Ожидаем 30 минут перед следующей проверкой

# Хэндлер для остановки уведомлений
@dp.message(Command("stop"))
async def stop_notification(message: Message):
    user_id = message.from_user.id
    # Логика удаления записи пользователя из базы
    await message.answer("Вы отписались от рассылки уведомлений.")

# Функция отправки уведомлений
async def send_telegram_notification(telegram_id: str, city: str, coordinates: str):
    await bot.send_message(telegram_id, f"Вы подписались на уведомления о загрязнении воздуха в городе {city}.\nКоординаты: {coordinates}")

# Запуск бота
async def start_bot():
    logging.info("Запуск бота...")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)  # Передаем bot в start_polling

# Функция on_startup для импорта в main.py
async def on_startup():
    logging.info("Бот запущен и готов к работе!")
    asyncio.create_task(send_notification())  # Запускаем функцию отправки уведомлений
