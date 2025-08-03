from aiogram import Dispatcher
from loader import dp, bot
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

# ثبت هندلرهای سایر فایل‌ها
from handlers.admin import register_admin_handlers
from handlers.gender import register_gender_handlers
from handlers.info import register_info_handlers
from handlers.profile import register_profile_handlers
from handlers.relationship import register_relationship_handlers
from handlers.crush import register_crush_handlers
from handlers.ship_logic import register_ship_handlers

# پیام خوش‌آمد به گروه
async def start_command(message: Message):
    if message.chat.type != "private":
        await message.reply("ربات فقط در چت خصوصی قابل استفاده است.")
        return

    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("من پسرم"), KeyboardButton("من دخترم"))
    markup.add(KeyboardButton("تعریف مشخصات"), KeyboardButton("شیپر من کیم؟"))
    markup.add(KeyboardButton("شروع شیپر 💘"))

    text = (
        "👋 به ربات شیپر فضوله خوش اومدی!\n\n"
        "📌 با استفاده از این ربات می‌تونی:\n"
        "- مشخصات خودتو ثبت کنی\n"
        "- جنسیت و سن و شهر رو وارد کنی\n"
        "- رفیق پیدا کنی یا کراش بزنی 😍\n"
        "- رل واقعی بزنی با تأیید طرف مقابل 💞\n"
        "- تبریک تولد و ماهگرد بگیری 🎉\n\n"
        "برای شروع یکی از گزینه‌ها رو انتخاب کن:"
    )

    await message.answer(text, reply_markup=markup)

def run():
    dp.register_message_handler(start_command, commands=["start"], state="*")

    # رجیستر سایر بخش‌ها
    register_admin_handlers(dp)
    register_gender_handlers(dp)
    register_info_handlers(dp)
    register_profile_handlers(dp)
    register_relationship_handlers(dp)
    register_crush_handlers(dp)
    register_ship_handlers(dp)
