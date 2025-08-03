# handlers/profile.py
from aiogram import types
from aiogram.dispatcher.filters import Text
from utils.db import load_group_data, save_group_data

# تعریف مشخصات: اسم، سن، قد، شهر
@dp.message_handler(lambda m: m.chat.type != "private" and m.text.lower().startswith("تعریف مشخصات"))
async def define_user_info(msg: types.Message):
    parts = msg.text.strip().split()
    if len(parts) != 6:
        await msg.reply("❗ فرمت درست: تعریف مشخصات اسم سن قد شهر\nمثال: تعریف مشخصات علی 20 175 تهران")
        return

    _, _, name, age, height, city = parts

    if not name.isalpha():
        await msg.reply("❗ نام باید فقط شامل حروف باشد.")
        return
    if not age.isdigit() or not height.isdigit():
        await msg.reply("❗ سن و قد باید عددی باشند.")
        return
    if not city.isalpha():
        await msg.reply("❗ شهر باید فقط شامل حروف باشد.")
        return

    data = load_group_data(msg.chat.id)
    uid = str(msg.from_user.id)
    data["users"].setdefault(uid, {})
    data["users"][uid].update({
        "name": name,
        "age": int(age),
        "height": int(height),
        "city": city
    })
    save_group_data(msg.chat.id, data)
    await msg.reply("✅ اطلاعات شما ثبت شد.")

# ثبت تولد شمسی
@dp.message_handler(lambda m: m.chat.type != "private" and m.text.lower().startswith("ثبت تولد"))
async def register_birthday(msg: types.Message):
    parts = msg.text.strip().split()
    if len(parts) != 3:
        await msg.reply("❗ فرمت درست: ثبت تولد روز/ماه/سال\nمثال: ثبت تولد 12/05/1382")
        return

    _, date = parts[0], parts[1]
    if not all(x.isdigit() for x in date.split("/")) or len(date.split("/")) != 3:
        await msg.reply("❗ تاریخ تولد باید با فرمت روز/ماه/سال وارد شود.")
        return

    data = load_group_data(msg.chat.id)
    uid = str(msg.from_user.id)
    data["users"].setdefault(uid, {})
    data["users"][uid]["birthday"] = date
    save_group_data(msg.chat.id, data)
    await msg.reply("✅ تاریخ تولد ثبت شد.")

# نمایش مشخصات کاربر
@dp.message_handler(Text(startswith="شیپر من کیم"))
async def show_user_profile(msg: types.Message):
    data = load_group_data(msg.chat.id)
    uid = str(msg.from_user.id)
    user = data["users"].get(uid)

    if not user:
        await msg.reply("❗ اطلاعاتی از شما ثبت نشده.")
        return

    profile = f"👤 مشخصات شما:\n"
    profile += f"• نام: {user.get('name', '-')}\n"
    profile += f"• سن: {user.get('age', '-')}\n"
    profile += f"• قد: {user.get('height', '-')}\n"
    profile += f"• شهر: {user.get('city', '-')}\n"
    profile += f"• جنسیت: {user.get('gender', '-')}\n"
    profile += f"• تولد: {user.get('birthday', '-')}\n"
    profile += f"• وضعیت: {user.get('status', '-')}\n"
    profile += f"• رل فعلی: {user.get('partner', '-')}\n"
    profile += f"• اکس: {user.get('ex', '-')}\n"

    await msg.reply(profile)
