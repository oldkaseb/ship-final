from aiogram import types
from aiogram.dispatcher.filters import Command
from loader import dp, bot
from utils.db import load_data, save_data
from config import ADMINS


# 📌 دستور: شیپر خروج
async def leave_group(msg: types.Message):
    if str(msg.from_user.id) not in ADMINS:
        return
    await msg.answer("ربات با موفقیت از گروه خارج شد ✅")
    await bot.leave_chat(msg.chat.id)


# 📌 دستور: شیپر لغو نصب
async def uninstall_shiper(msg: types.Message):
    if str(msg.from_user.id) not in ADMINS:
        return
    data = load_data(msg.chat.id)
    data["installed"] = False
    save_data(msg.chat.id, data)
    await msg.reply("✅ شیپر با موفقیت لغو نصب شد. برای فعال‌سازی دوباره از دستور 'شیپر نصب' استفاده کنید.")


# 📌 دستور: شیپر نصب
async def install_shiper(msg: types.Message):
    if str(msg.from_user.id) not in ADMINS:
        return
    data = load_data(msg.chat.id)
    data["installed"] = True
    data["owner_id"] = msg.from_user.id
    save_data(msg.chat.id, data)
    await msg.reply("✅ شیپر در این گروه نصب شد. حالا از دستورات استفاده کن!")


# 📌 دستور: شیپر پنل (فقط برای ادمین اصلی)
async def show_admin_panel(msg: types.Message):
    if str(msg.from_user.id) not in ADMINS:
        return
    await msg.reply("🔧 پنل ادمین فعال است!\nاز دستورات مدیریتی استفاده کنید.")


# 📌 ثبت فروشنده یا ادمین گروه (شیپر فروشنده 123456)
async def set_admin(msg: types.Message):
    if str(msg.from_user.id) not in ADMINS:
        return
    parts = msg.text.split()
    if len(parts) != 3:
        await msg.reply("فرمت صحیح: شیپر فروشنده user_id")
        return
    _, _, new_admin_id = parts
    data = load_data(msg.chat.id)
    admins = data.get("settings", {}).get("admins", [])
    if new_admin_id not in admins:
        admins.append(new_admin_id)
    data.setdefault("settings", {})["admins"] = admins
    save_data(msg.chat.id, data)
    await msg.reply(f"✅ آیدی {new_admin_id} به‌عنوان فروشنده اضافه شد.")


# 📌 تابع ثبت هندلرها
def register_admin_handlers(dp):
    dp.register_message_handler(install_shiper, lambda msg: msg.text.lower() == "شیپر نصب")
    dp.register_message_handler(uninstall_shiper, lambda msg: msg.text.lower() == "شیپر لغو نصب")
    dp.register_message_handler(leave_group, lambda msg: msg.text.lower() == "شیپر خروج")
    dp.register_message_handler(show_admin_panel, lambda msg: msg.text.lower() == "شیپر پنل")
    dp.register_message_handler(set_admin, lambda msg: msg.text.startswith("شیپر فروشنده"))
