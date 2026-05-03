import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from flask import Flask
from threading import Thread

# MA'LUMOTLAR
API_TOKEN = '8735644958:AAHBhZo0mDiDqamaW96S_DJQJ0ct2FF6-sc'
CH_ID = -1003981288701  
CH_LINK = "https://t.me/+FiSw2naU1_oyY2Uy"

# Logging
logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# --- RENDER UCHUN PORT QISMI (MUHIM!) ---
app = Flask('')

@app.route('/')
def home():
    return "Bot is running!"

def run():
    # Render portni o'zi beradi, biz shunchaki uni tinglaymiz
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()
# ---------------------------------------

def check_sub_markup():
    markup = InlineKeyboardMarkup(row_width=1)
    btn = InlineKeyboardButton(text="Kanalga a'zo bo'lish ➕", url=CH_LINK)
    check_btn = InlineKeyboardButton(text="Obunani tekshirish ✅", callback_data="check_subs")
    markup.add(btn, check_btn)
    return markup

@dp.message_handler(commands=['start'])
async def start_cmd(message: types.Message):
    user_id = message.from_user.id
    try:
        check = await bot.get_chat_member(chat_id=CH_ID, user_id=user_id)
        if check.status != 'left':
            await message.answer(f"Xush kelibsiz! Botdan foydalanishingiz mumkin. 😊")
        else:
            await message.answer("Botdan foydalanish uchun kanalimizga obuna bo'ling! 👇", reply_markup=check_sub_markup())
    except Exception as e:
        await message.answer("Xatolik! Bot kanalda admin ekanligini tekshiring.")

@dp.callback_query_handler(text="check_subs")
async def check_callback(call: types.CallbackQuery):
    user_id = call.from_user.id
    try:
        check = await bot.get_chat_member(chat_id=CH_ID, user_id=user_id)
        if check.status != 'left':
            await call.answer("Rahmat! Obuna tasdiqlandi. ✅", show_alert=True)
            await call.message.edit_text("Xush kelibsiz! Endi botni ishlatishingiz mumkin. 🚀")
        else:
            await call.answer("Siz hali kanalga a'zo bo'lmadingiz! ✨", show_alert=True)
    except Exception:
        await call.answer("Botni kanalda admin qiling! ❌", show_alert=True)

if __name__ == '__main__':
    keep_alive() # Veb-serverni ishga tushirish
    executor.start_polling(dp, skip_updates=True) # Botni ishga tushirish
