from aiogram import types
from utils.db import load_data, save_data

async def ship_user(message: types.Message):
    chat_id = str(message.chat.id)
    user_id = str(message.from_user.id)

    data = load_data(chat_id)
    users = data.get("users", {})
    crushes = data.get("crushes", {})

    # بررسی وجود اطلاعات کاربر
    if user_id not in users or "gender" not in users[user_id]:
        await message.reply("برای شیپ شدن اول باید جنسیت و مشخصاتت رو ثبت کنی 📝")
        return

    user_gender = users[user_id].get("gender")
    crush_list = crushes.get(user_id, [])

    # حالت اول: شیپ با یکی از کراش‌ها
    if crush_list:
        target_id = random.choice(crush_list)
        if target_id in users:
            partner = users[target_id]
            await message.reply(
                f"🎉 شما با کراشت شیپ شدی!\n"
                f"{partner.get('name', 'ناشناس')} ❤️ {users[user_id].get('name', 'تو')}\n"
                f"از امروز یه کاپل جدید داریم 💑"
            )
            return

    # حالت دوم: شیپ تصادفی با جنس مخالف
    opposite_gender = "دختر" if user_gender == "پسر" else "پسر"
    eligible = [
        uid for uid, uinfo in users.items()
        if uid != user_id and uinfo.get("gender") == opposite_gender
    ]

    if eligible:
        target_id = random.choice(eligible)
        partner = users[target_id]
        await message.reply(
            f"💘 شیپ تصادفی با فردی از جنس مخالف:\n"
            f"{users[user_id].get('name', 'تو')} ❤️ {partner.get('name', 'طرف مقابل')}\n"
            f"مواظب قلباتون باشین! 💓"
        )
    else:
        await message.reply("متأسفم، هیچ کاربری از جنس مخالف برای شیپ موجود نیست 😢")
