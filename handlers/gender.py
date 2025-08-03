# handlers/gender.py
from aiogram import types
from utils.db import load_group_data, save_group_data

async def handle_gender(message: types.Message):
    if message.chat.type == "private":
        return

    text = message.text.lower()
    user_id = str(message.from_user.id)
    chat_id = message.chat.id

    if "من پسرم" in text:
        gender = "پسر"
    elif "من دخترم" in text:
        gender = "دختر"
    else:
        return

    data = load_group_data(chat_id)
    if user_id not in data["users"]:
        data["users"][user_id] = {}

    data["users"][user_id]["gender"] = gender
    save_group_data(chat_id, data)

    await message.reply(f"جنسیت شما به‌عنوان {gender} ثبت شد ✅")
