import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

# --- SOZLAMALAR ---
API_TOKEN = '8158239113:AAEg9b2m5Lx0GYs6WaKGwU1sdSn5I3TStwg' 
ADMIN_ID = 5354687056 
CHANNELS = ["@DJ_Baxtiyor"] 
WEBSITE_URL = "https://leofame.com/free-instagram-views" 

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

async def check_sub(user_id):
    for channel in CHANNELS:
        try:
            member = await bot.get_chat_member(chat_id=channel, user_id=user_id)
            if member.status == 'left': return False
        except: return False
    return True

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    if await check_sub(message.from_user.id):
        # Sayt tugmasi
        btn = InlineKeyboardMarkup().add(
            InlineKeyboardButton("Saytni ochish", web_app=WebAppInfo(url=WEBSITE_URL))
        )
        await message.answer("Xush kelibsiz! Pastdagi tugma orqali saytga kiring:", reply_markup=btn)
    else:
        # A'zo bo'lish tugmasi
        btn = InlineKeyboardMarkup(row_width=1)
        btn.add(
            InlineKeyboardButton("Kanalga a'zo bo'lish", url=f"https://t.me/{CHANNELS[0][1:]}"),
            InlineKeyboardButton("Tekshirish ✅", callback_data="check")
        )
        await message.answer("Botdan foydalanish uchun kanalimizga a'zo bo'ling:", reply_markup=btn)

@dp.callback_query_handler(text="check")
async def check_callback(call: types.CallbackQuery):
    if await check_sub(call.from_user.id):
        await call.message.delete()
        await start(call.message)
    else:
        await call.answer("Siz hali a'zo bo'lmadingiz!", show_alert=True)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
