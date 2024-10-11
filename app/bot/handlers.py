# from aiogram import types
# from aiogram.dispatcher import Dispatcher
# from db.database import SessionLocal
# from db.models import Subscription

# async def save_user_data(user_id, city, lon, lat):
#     async with SessionLocal() as session:
#         async with session.begin():
#             new_sub = Subscription(user_id=user_id, city=city, lon=lon, lat=lat)
#             session.add(new_sub)
#         await session.commit()

# async def remove_user(user_id):
#     async with SessionLocal() as session:
#         await session.execute(f"DELETE FROM subscriptions WHERE user_id = {user_id}")
#         await session.commit()

# async def start_handler(message: types.Message):
#     args = message.get_args()
#     params = {p.split('=')[0]: p.split('=')[1] for p in args.split('&')}
    
#     city = params.get('city')
#     lon = float(params.get('lon'))
#     lat = float(params.get('lat'))
#     user_id = message.from_user.id

#     await save_user_data(user_id, city, lon, lat)

#     await message.reply("Спасибо за подписку на рассылку! Теперь вы будете получать уведомления о качестве воздуха.", parse_mode=types.ParseMode.MARKDOWN)

# async def stop_handler(message: types.Message):
#     user_id = message.from_user.id
#     await remove_user(user_id)

#     await message.reply("Вы успешно отписались от уведомлений.", parse_mode=types.ParseMode.MARKDOWN)

# def register_handlers(dp: Dispatcher):
#     dp.register_message_handler(start_handler, commands=['start'])
#     dp.register_message_handler(stop_handler, commands=['stop'])
