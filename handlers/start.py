from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from loader import dp, bot
from handlers.admin import register_admin_handlers
from handlers.crush import register_crush_handlers
from handlers.gender import register_gender_handlers
from handlers.info import register_info_handlers
from handlers.profile import register_profile_handlers
from handlers.relationship import register_relationship_handlers
from handlers.ship_logic import register_ship_logic_handlers
from utils.db import load_data
import logging


# ✅ استارت ربات در پی‌وی
@dp.message_handler(commands=["start"])
async def private_start(msg: types.Message):
    if msg.chat.type != "private":
        return

    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(
        InlineKeyboardButton("📋 راهنما", callback_data="help"),
        InlineKeyboardButton("📞 تماس با مالک", url="https://t.me/oldkaseb"),
        InlineKeyboardButton("➕ افزودن ربات به گروه", url=f"https://t.me/{(await bot.get_me()).username}?startgroup=true")
    )

    await msg.answer(
        """👋 به ربات شیپر فضوله خوش اومدی!

✨ با امکانات پیشرفته برای شیپ‌سازی، کراش، ثبت مشخصات، تولد، رل و...

💸 قیمت شارژ ماهیانه: ۵۰ هزار تومان
🆓 تست رایگان ۷ روزه برای گروه‌های جدید

🔽 برای شروع یکی از گزینه‌های زیر رو بزن:""",
        reply_markup=kb
    )


# ✅ هندلر کلیک راهنما
@dp.callback_query_handler(lambda c: c.data == "help")
async def send_help(call: types.CallbackQuery):
    await call.message.edit_text(
        "📚 راهنمای ربات:\n"
        "- من پسرم / من دخترم → ثبت جنسیت\n"
        "- تعریف مشخصات اسم سن قد شهر\n"
        "- ثبت تولد 12/05/1383\n"
        "- شیپر من کیم → نمایش اطلاعات شما\n"
        "- شیپم کن / ثبت کراش / شیپر کات\n"
        "- شیپر نصب / شیپر پنل / شیپر خروج\n"
        "و کلی امکانات دیگه..."
    )
    await call.answer()


# ✅ تابع برای ثبت تمام هندلرها
def run(dp):
    try:
        register_admin_handlers(dp)
        register_crush_handlers(dp)
        register_gender_handlers(dp)
        register_info_handlers(dp)
        register_profile_handlers(dp)
        register_relationship_handlers(dp)
        register_ship_logic_handlers(dp)
    except Exception as e:
        logging.error(f"❌ Error while registering handlers: {e}")
