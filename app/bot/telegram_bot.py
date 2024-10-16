from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import Command
from aiogram.types import Message
import asyncio
import logging
from dotenv import load_dotenv
import os
from app.db.database import get_db
import app.db.crud as crud
from air_quality import get_city_by_coords

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

# Логирование
logging.basicConfig(level=logging.INFO)

# Создание экземпляра бота
bot = Bot(token=TELEGRAM_BOT_TOKEN)
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
        try:
            # Извлекаем координаты из сообщения
            lon = message.text.split("lon")[1].split("lat")[0].strip()
            lat = message.text.split("lat")[1].strip()

            lon = float(lon.replace("-", "."))  # Преобразуем строку в float
            lat = float(lat.replace("-", "."))

            # Вместо геокодера по умолчанию город Астрахань - исправлено
            city = await get_city_by_coords(lat, lon)

            with get_db() as db:
                telegram_id = message.from_user.id
                # Используем функцию create_or_update_subscription
                crud.create_or_update_subscription(
                    db,
                    telegram_id=telegram_id,
                    city=city,
                    lon=lon,
                    lat=lat
                )

            await message.answer(f"Спасибо за подписку на рассылку!\nГород: {city}\nКоординаты: {lon}, {lat}")

        except ValueError as e:
            logging.error(f"Ошибка: {e}")
            await message.answer(f"Подписка уже существует. Ваши данные были обновлены.\nГород: {city}\nКоординаты: {lon}, {lat}")

        except Exception as e:
            logging.error(f"Произошла ошибка: {e}")
            await message.answer("Произошла ошибка при обработке координат. Пожалуйста, проверьте формат и попробуйте снова.")
    
    else:
        await message.answer("Пожалуйста, укажите координаты в формате: /start lon36.19lat51.73")

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