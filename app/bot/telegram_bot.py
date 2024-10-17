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
from air_quality import get_city_by_coords, get_air_pollution_data

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
async def send_notifications():
    logging.info("Функция send_notifications запущена")
    while True:
        try:
            # Логика пробежки по базе данных и проверки условий загрязнения
            with get_db() as db:
                users = crud.get_all_subscriptions(db)  # Получаем всех подписчиков
                logging.info(f"Получено {len(users)} подписчиков")
                for user in users:
                    user_id = user.telegram_id
                    city = user.city
                    lon = user.lon
                    lat = user.lat

                    await bot.send_message(user_id, f"Внимание! В городе {city} превышен уровень загрязнения!")
                    # Получаем данные о качестве воздуха
                    air_data = await get_air_pollution_data(lat, lon)

                    # Проверяем, если уровень загрязнения превышает допустимые нормы
                    # if air_data and air_data['list'][0]['main']['aqi'] > 2:  # Пример проверки
                    # await bot.send_message(user_id, f"Внимание! В городе {city} превышен уровень загрязнения!")
        except Exception as e:
            logging.error(f"Ошибка в функции отправки уведомлений: {e}")
        await asyncio.sleep(10)  # Ожидаем 30 минут перед следующей проверкой

# Хэндлер команды /stop
@dp.message(Command("stop"))
async def stop(message: Message):
    with get_db() as db:
        success = crud.delete_subscription(db, telegram_id=message.from_user.id)
        if success:
            await message.answer("Вы отписались от уведомлений.")
        else:
            await message.answer("Вы не были подписаны на уведомления.")

# Запуск бота
async def start_bot():
    logging.info("Запуск бота...")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)  # Передаем bot в start_polling