# handlers/crush.py
from aiogram import types
from aiogram.dispatcher import filters
from utils.db import load_data, save_data
from random import choice

# ثبت کراش از طریق ریپلای، منشن، یوزرنیم یا آیدی عددی
async def add_crush(msg: types.Message):
    data = load_data(msg.chat.id)
    user_id = str(msg.from_user.id)
    if user_id not in data["users"]:
        await msg.reply("اول باید اطلاعات خودتو ثبت کنی.")
        return

    if msg.reply_to_message:
        target_id = str(msg.reply_to_message.from_user.id)
    else:
        parts = msg.text.split()
        if len(parts) < 2:
            await msg.reply("برای ثبت کراش باید آیدی عددی، یوزرنیم یا منشن بدی یا ریپلای کنی.")
            return
        arg = parts[1]
        if arg.startswith("@"):
            for uid, info in data["users"].items():
                if info.get("username", "").lower() == arg[1:].lower():
                    target_id = uid
                    break
            else:
                await msg.reply("کاربری با این یوزرنیم پیدا نشد.")
                return
        elif arg.isdigit():
            target_id = arg
        else:
            await msg.reply("فرمت نامعتبر.")
            return

    if target_id == user_id:
        await msg.reply("نمیشه خودتو کراش بزنی 😅")
        return

    data["crushes"].setdefault(user_id, [])
    if target_id in data["crushes"][user_id]:
        await msg.reply("این کاربر از قبل کراش تو هست.")
    else:
        data["crushes"][user_id].append(target_id)
        await msg.reply("کراش ثبت شد 😎")

    save_data(msg.chat.id, data)

# حذف کراش
async def remove_crush(msg: types.Message):
    data = load_data(msg.chat.id)
    user_id = str(msg.from_user.id)

    if msg.reply_to_message:
        target_id = str(msg.reply_to_message.from_user.id)
    else:
        parts = msg.text.split()
        if len(parts) < 2:
            await msg.reply("برای حذف کراش باید آیدی عددی، یوزرنیم یا منشن بدی یا ریپلای کنی.")
            return
        arg = parts[1]
        if arg.startswith("@"):
            for uid, info in data["users"].items():
                if info.get("username", "").lower() == arg[1:].lower():
                    target_id = uid
                    break
            else:
                await msg.reply("یوزرنیم نامعتبر.")
                return
        elif arg.isdigit():
            target_id = arg
        else:
            await msg.reply("فرمت نادرست.")
            return

    if user_id in data["crushes"] and target_id in data["crushes"][user_id]:
        data["crushes"][user_id].remove(target_id)
        await msg.reply("کراش حذف شد 🗑️")
    else:
        await msg.reply("کراشی با این مشخصات پیدا نشد.")

    save_data(msg.chat.id, data)

# نمایش لیست کراش‌های کاربر
async def list_crushes(msg: types.Message):
    data = load_data(msg.chat.id)
    user_id = str(msg.from_user.id)
    crushes = data["crushes"].get(user_id, [])

    if not crushes:
        await msg.reply("هنوز کسی کراش تو نیست 😔")
        return

    text = "💘 لیست کراش‌های شما:\n"
    for cid in crushes:
        info = data["users"].get(cid, {})
        text += f"• {info.get('name', 'نامشخص')} ({info.get('username', 'ID: ' + cid)})\n"
    await msg.reply(text)

# شیپ‌سازی با یکی از کراش‌ها یا یک فرد تصادفی از جنس مخالف
async def ship_me(msg: types.Message):
    data = load_data(msg.chat.id)
    user_id = str(msg.from_user.id)
    user = data["users"].get(user_id)

    if not user or "gender" not in user:
        await msg.reply("اول باید جنسیتتو ثبت کنی.")
        return

    crush_list = data["crushes"].get(user_id, [])
    target_id = None

    if crush_list:
        target_id = choice(crush_list)
    else:
        opposite_gender = "پسر" if user["gender"] == "دختر" else "دختر"
        candidates = [uid for uid, u in data["users"].items() if u.get("gender") == opposite_gender and uid != user_id]
        if not candidates:
            await msg.reply("کسی برای شیپ‌سازی پیدا نشد 😕")
            return
        target_id = choice(candidates)

    partner = data["users"].get(target_id, {})
    text = f"❤️‍🔥 شیپ جدید!\n{user.get('name', 'شما')} ❤️ {partner.get('name', 'یه نفر خاص')}\n"
    await msg.reply(text)

# ثبت هندلرها
def register_crush_handlers(dp):
    dp.register_message_handler(add_crush, lambda m: m.chat.type != "private" and m.text.lower().startswith("ثبت کراش"))
    dp.register_message_handler(remove_crush, lambda m: m.chat.type != "private" and m.text.lower().startswith("حذف کراش"))
    dp.register_message_handler(list_crushes, lambda m: m.chat.type != "private" and m.text.lower().startswith("لیست کراش"))
    dp.register_message_handler(ship_me, lambda m: m.chat.type != "private" and m.text.lower().startswith("شیپم کن"))
