from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import OWNER_ID, BOT_NAME

# دکمه‌های منوی استارت
def start_keyboard():
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton("📌 افزودن به گروه", url="https://t.me/FOSOOL_BOT?startgroup=start"),
        InlineKeyboardButton("📖 راهنمای دستورات", callback_data="help")
    )
    kb.add(
        InlineKeyboardButton("👑 تماس با مالک", url=f"https://t.me/{get_username_from_id(OWNER_ID)}")
    )
    return kb

# تبدیل آیدی به یوزرنیم برای لینک مالک
def get_username_from_id(user_id: int) -> str:
    return "oldkaseb"  # اگر نیاز بود در آینده، داینامیک کنیم

# پیام استارت
async def start_cmd(message: types.Message):
    if message.chat.type != "private":
        return  # فقط در پیوی پاسخ می‌ده

    text = (
        f"سلام خوش اومدی به <b>{BOT_NAME}</b> 😎\n\n"
        "من یه ربات اجتماعی‌ام که روابط بین اعضای گروهت رو مدیریت می‌کنم 💞\n"
        "از رل‌زدن و کراش گرفته تا تولد و شیپ شبانه 🎉\n\n"
        "برای شروع، منو به گروهت اضافه کن و دسترسی‌های زیر رو بده:\n"
        "🟢 حذف پیام‌ها\n🟢 خواندن پیام‌ها\n🟢 منشن اعضا\n🟢 دسترسی ادمین\n\n"
        "با کلیک روی دکمه‌های زیر شروع کن 👇"
    )
    await message.answer(text, reply_markup=start_keyboard())

# جلوگیری از پاسخ در گروه‌ها
async def block_in_group(message: types.Message):
    if message.chat.type != "private":
        return  # در گروه هیچ پاسخی نمی‌ده

# دکمه راهنما (callback)
async def help_callback(call: types.CallbackQuery):
    await call.message.edit_text(
        "🛠 راهنمای استفاده از ربات:\n"
        "- دستورات متنی و ساده‌ان، بدون /کامند\n"
        "- فقط در گروه جواب می‌دم (مگر استارت)\n"
        "- توی گروه، بپرس: کی منو می‌خواد؟ 😅\n"
        "- یا بگو: کراشم @username\n"
        "- هر شب ساعت ۹ شیپ می‌کنم 👩‍❤️‍👨\n"
        "- با ریپلای می‌تونی مشخصات ثبت کنی\n"
        "- فقط با عضویت در گروه فعال می‌شم\n\n"
        "❤️ با من خوش بگذره!"
    )

def register_handlers(dp: Dispatcher):
    dp.register_message_handler(start_cmd, commands=["start"], state="*")
    dp.register_message_handler(block_in_group, chat_type=["group", "supergroup"])
    dp.register_callback_query_handler(help_callback, text="help")
