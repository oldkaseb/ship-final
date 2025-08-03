# handlers/admin.py

from aiogram import types
from datetime import datetime, timedelta
from utils.db import load_data, save_data
from aiogram.dispatcher.filters import Text
from loader import dp, bot

OWNER_ID = 7662192190  # آی‌دی سازنده ربات (@oldkaseb)

@dp.message_handler(Text(equals="شیپر نصب"))
async def install_bot(msg: types.Message):
    if msg.chat.type == "private":
        return

    data = load_data(msg.chat.id)
    if data.get("installed"):
        await msg.reply("✅ ربات قبلاً در این گروه نصب شده.")
        return

    data["installed"] = True
    data["owner_id"] = msg.from_user.id
    data["expiration"] = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
    data["users"] = {}
    data["crushes"] = {}
    data["couples"] = []
    data["settings"] = {
        "admins": [msg.from_user.id],
        "required_channel": None
    }

    save_data(msg.chat.id, data)
    await msg.reply("✅ ربات با موفقیت نصب شد.\n📅 تست رایگان ۷ روزه فعال شد.")

    try:
        invite_link = await bot.export_chat_invite_link(msg.chat.id)
        await bot.send_message(OWNER_ID, f"📌 گروه جدید:\n{msg.chat.title}\n{invite_link}")
    except:
        pass


@dp.message_handler(Text(equals="شیپر لغو نصب"))
async def uninstall_bot(msg: types.Message):
    if msg.chat.type != "supergroup":
        return

    data = load_data(msg.chat.id)
    if msg.from_user.id != data.get("owner_id"):
        return await msg.reply("❌ فقط مالک می‌تواند نصب را لغو کند.")

    data["installed"] = False
    save_data(msg.chat.id, data)
    await msg.reply("❌ نصب ربات لغو شد. اطلاعات ذخیره باقی می‌ماند.")


@dp.message_handler(Text(equals="شیپر خروج"))
async def leave_group(msg: types.Message):
    if msg.chat.type != "supergroup":
        return
    await msg.reply("👋 خداحافظ! ربات از گروه خارج می‌شود.")
    await bot.leave_chat(msg.chat.id)


@dp.message_handler(Text(startswith="شیپر شارژ"))
async def charge_group(msg: types.Message):
    if msg.chat.type != "supergroup":
        return

    data = load_data(msg.chat.id)
    if msg.from_user.id not in [data.get("owner_id"), OWNER_ID]:
        return await msg.reply("❌ فقط مالک اصلی یا فروشنده می‌تواند گروه را شارژ کند.")

    extra_days = 30
    if len(msg.text.split()) >= 3:
        try:
            extra_days = int(msg.text.split()[2])
        except:
            pass

    expire_date = datetime.strptime(data.get("expiration"), "%Y-%m-%d")
    new_expire = (expire_date + timedelta(days=extra_days)).strftime("%Y-%m-%d")
    data["expiration"] = new_expire
    save_data(msg.chat.id, data)

    await msg.reply(f"✅ گروه برای {extra_days} روز شارژ شد.\n📅 تا تاریخ {new_expire}")


@dp.message_handler(commands=["check_exp"])
async def check_expiration(msg: types.Message):
    data = load_data(msg.chat.id)
    expire_str = data.get("expiration")
    expire_date = datetime.strptime(expire_str, "%Y-%m-%d")
    days_left = (expire_date - datetime.now()).days

    if days_left <= 2:
        await msg.reply("⏳ تنها ۲ روز تا پایان تست رایگان باقی‌مانده است.\nبرای تمدید از دستور «شیپر شارژ» استفاده کنید.")
