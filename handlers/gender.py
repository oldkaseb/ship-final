from aiogram import types, Dispatcher
from aiogram.types import Message
from utils.db import load_group_data, save_group_data
from loader import dp

async def set_gender(message: Message):
    # تشخیص جنسیت
    if message.text == "من پسرم":
        gender = "پسر"
    elif message.text == "من دخترم":
        gender = "دختر"
    else:
        return

    group_id = str(message.chat.id)
    user_id = str(message.from_user.id)

    # بارگذاری داده‌های گروه
    data = load_group_data(group_id)
    if "users" not in data:
        data["users"] = {}
    if user_id not in data["users"]:
        data["users"][user_id] = {}

    # ذخیره جنسیت
    data["users"][user_id]["gender"] = gender
    save_group_data(group_id, data)

    await message.reply(f"جنسیت شما به عنوان «{gender}» ثبت شد ✅")

def register_gender_handlers(dp: Dispatcher):
    dp.register_message_handler(set_gender, lambda message: message.text in ["من پسرم", "من دخترم"], state="*")
