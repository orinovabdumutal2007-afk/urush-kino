import telebot
from telebot import types

# --- ASOSIY SOZLAMALAR ---
# Token va ID larni o'zgartirmasdan saqlang
TOKEN = '8735644958:AAHBhZo0mDiDqamaW96S_DJQJ0ct2FF6-sc'
ADMIN_ID = 6655098949
CHANNEL_ID = -1002447952136  # Kanalning raqamli ID si
PRIVATE_LINK = "https://t.me/+FiSw2naU1_oyY2Uy" # Kirish so'rovi uchun link

bot = telebot.TeleBot(TOKEN)

# --- FUNKSIYALAR ---

def check_sub(user_id):
    """Foydalanuvchi kanalga so'rov yuborgan yoki a'zo ekanini tekshiradi"""
    try:
        member = bot.get_chat_member(CHANNEL_ID, user_id)
        # Agar a'zo bo'lsa yoki admin bo'lsa True qaytaradi
        if member.status in ['member', 'administrator', 'creator']:
            return True
        return False
    except Exception as e:
        # Xatolik bo'lsa (masalan bot admin bo'lmasa) False qaytaradi
        print(f"Xatolik: {e}")
        return False

# --- START KOMANDASI ---

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    
    if check_sub(user_id):
        # OBUNA BO'LGANLAR UCHUN ASOSIY MENYU
        markup = types.InlineKeyboardMarkup(row_width=2)
        btn_search = types.InlineKeyboardButton("🔍 Kino qidirish", callback_data="search_kino")
        btn_genres = types.InlineKeyboardButton("📂 Janrlar", callback_data="show_genres")
        markup.add(btn_search, btn_genres)
        
        if user_id == ADMIN_ID:
            markup.add(types.InlineKeyboardButton("⚙️ Admin Panel", callback_data="admin_panel"))
            
        bot.send_message(message.chat.id, f"Salom {message.from_user.first_name}! Botdan foydalanishingiz mumkin. 👇", reply_markup=markup)
    else:
        # OBUNA BO'LMAGANLAR UCHUN "1-KANAL" BLOKIROVKASI
        markup = types.InlineKeyboardMarkup()
        btn_link = types.InlineKeyboardButton("📢 1-kanal (So'rov yuboring)", url=PRIVATE_LINK)
        btn_check = types.InlineKeyboardButton("✅ Tekshirish", callback_data="check_subscription")
        markup.add(btn_link)
        markup.add(btn_check)
        
        bot.send_message(message.chat.id, "Botni ishga tushirish uchun kanalga so'rov yuboring va 'Tekshirish' tugmasini bosing! 🔐", reply_markup=markup)

# --- TUGMALAR ISHLASHI (CALLBACK) ---

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    user_id = call.from_user.id
    
    if call.data == "check_subscription":
        if check_sub(user_id):
            bot.answer_callback_query(call.id, "Tabriklaymiz! Endi botdan foydalanishingiz mumkin. ✅")
            bot.delete_message(call.message.chat.id, call.message.message_id)
            start(call.message)
        else:
            bot.answer_callback_query(call.id, "Siz hali so'rov yubormadingiz yoki so'rovingiz tasdiqlanmadi! ❌", show_alert=True)
            
    elif call.data == "search_kino":
        bot.send_message(call.message.chat.id, "Kino kodini yuboring:")

    elif call.data == "admin_panel" and user_id == ADMIN_ID:
        markup = types.InlineKeyboardMarkup()
        btn_poll = types.InlineKeyboardButton("📊 10k haqida so'rovnoma", callback_data="send_poll")
        markup.add(btn_poll)
        bot.send_message(call.message.chat.id, "Admin panel:", reply_markup=markup)

    elif call.data == "send_poll" and user_id == ADMIN_ID:
        bot.send_poll(
            call.message.chat.id, 
            "Kanalni 10k bo'lganda sotaylikmi?", 
            ["Ha, soting ✅", "Yo'q, sotmang ❌"], 
            is_anonymous=False
        )

# --- MATNLI XABARLAR (KINO KODLARI) ---

@bot.message_handler(func=lambda message: True)
def handle_text(message):
    user_id = message.from_user.id
    
    if check_sub(user_id):
        # Kino kodlarini tekshirish
        if message.text == "101":
            bot.reply_to(message, f"🎬 'Forsaj 10' filmi: {PRIVATE_LINK}")
        elif message.text == "777":
            bot.reply_to(message, f"🎬 'Fight Club' filmi: {PRIVATE_LINK}")
        else:
            bot.reply_to(message, "Kino topilmadi. Kodni to'g'ri kiriting. 😔")
    else:
        # Obuna bo'lmagan bo'lsa start menyusiga qaytaradi
        start(message)

# --- SO'ROVLARNI AVTOMAT QABUL QILISH ---

@bot.chat_join_request_handler()
def handle_join_request(request):
    try:
        bot.approve_chat_join_request(request.chat.id, request.from_user.id)
        bot.send_message(request.from_user.id, "So'rovingiz tasdiqlandi! Botdan foydalanishingiz mumkin. 🚀")
    except Exception as e:
        print(f"Xato: {e}")

# --- BOTNI YURGIZISH ---
bot.infinity_polling(none_stop=True)
      
async def check_sub(user_id):
    for channel in CHANNELS:
        try:
            # Kanal nomini @ belgisiz ham, bilan ham qabul qilish uchun
            chat_id = channel if channel.startswith("@") else f"@{channel}"
            member = await bot.get_chat_member(chat_id=chat_id, user_id=user_id)
            
            # Agar foydalanuvchi quyidagi statuslarda bo'lmasa, demak u a'zo emas
            # 'member', 'administrator', 'creator' - bular a'zolikni bildiradi
            if member.status not in ["member", "administrator", "creator"]:
                return False
        except Exception as e:
            print(f"Xatolik yuz berdi: {e}")
            # Agar bot admin bo'lmasa yoki kanal topilmasa ham False qaytaradi
            return False
    return True
        
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Ma'lumotlaringiz kiritildi ✅
API_TOKEN = '8735644958:AAHBhZo0mDiDqamaW96S_DJQJ0ct2FF6-sc'
CH_ID = -1003981288701  
CH_LINK = "https://t.me/+FiSw2naU1_oyY2Uy"

# Loggingni sozlash (xatolarni ko'rish uchun)
logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Obuna tugmalarini yaratish
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
        # Kanal a'zoligini tekshirish
        check = await bot.get_chat_member(chat_id=CH_ID, user_id=user_id)
        
        if check.status != 'left':
            await message.answer(f"Xush kelibsiz! Botdan foydalanishingiz mumkin. 😊")
        else:
            await message.answer(
                "Botdan foydalanish uchun kanalimizga obuna bo'ling! 👇", 
                reply_markup=check_sub_markup()
            )
    except Exception as e:
        # Agar bot kanalga admin bo'lmasa yoki ID xato bo'lsa
        logging.error(f"Xatolik yuz berdi: {e}")
        await message.answer("Xatolik yuz berdi. Bot kanalda admin ekanligini tekshiring!")

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
    executor.start_polling(dp, skip_updates=True)
    
