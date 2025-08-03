# handlers/relationship.py
from aiogram import types
from aiogram.dispatcher import Dispatcher
from utils.db import load_data, save_data

dp: Dispatcher = None  # در main.py مقداردهی می‌شود

def set_dispatcher(dispatcher):
    global dp
    dp = dispatcher
    register_handlers()

def register_handlers():
    dp.register_message_handler(register_relationship, lambda m: m.chat.type != "private" and m.text.lower().startswith("من رلم شیپر"))
    dp.register_message_handler(register_single, lambda m: m.chat.type != "private" and "من سینگلم شیپر" in m.text.lower())
    dp.register_message_handler(remove_relationship, lambda m: m.chat.type != "private" and "شیپر کات" in m.text.lower())
    dp.register_message_handler(manual_partner, lambda m: m.chat.type != "private" and (m.text.startswith("ثبت پارتنر") or m.text.startswith("ثبت اکس")))

async def register_relationship(msg: types.Message):
    data = load_data(msg.chat.id)
    uid = str(msg.from_user.id)

    parts = msg.text.split()
    if len(parts) < 4:
        await msg.reply("لطفاً آیدی عددی یا یوزرنیم یا منشن پارتنرت رو بعد از دستور وارد کن.\nمثال: من رلم شیپر @user123")
        return

    partner_raw = parts[3]
    partner_id = None

    if msg.entities and len(msg.entities) > 1:
        ent = msg.entities[1]
        if ent.type == "mention":
            username = msg.text[ent.offset: ent.offset + ent.length].lstrip("@")
            for user_id, info in data["users"].items():
                if info.get("username") == username:
                    partner_id = user_id
                    break
    elif partner_raw.isdigit():
        partner_id = partner_raw
    else:
        await msg.reply("نتونستم پارتنرتو شناسایی کنم 😕")
        return

    if not partner_id:
        await msg.reply("پارتنری با این مشخصات پیدا نشد.")
        return

    data["users"].setdefault(uid, {})["partner"] = partner_id
    data["users"].setdefault(partner_id, {})["partner"] = uid
    data["users"][uid]["relationship_since"] = msg.date.strftime("%Y-%m-%d")
    data["users"][partner_id]["relationship_since"] = msg.date.strftime("%Y-%m-%d")
    save_data(msg.chat.id, data)

    await msg.reply(f"❤️ تبریک! شما و [{partner_id}](tg://user?id={partner_id}) حالا یک زوج هستید!", parse_mode="Markdown")

async def register_single(msg: types.Message):
    data = load_data(msg.chat.id)
    uid = str(msg.from_user.id)

    data["users"].setdefault(uid, {})["partner"] = None
    data["users"][uid]["relationship_since"] = None
    save_data(msg.chat.id, data)
    await msg.reply("حالت به سینگل تغییر کرد ✅")

async def remove_relationship(msg: types.Message):
    data = load_data(msg.chat.id)
    uid = str(msg.from_user.id)
    user = data["users"].get(uid)

    if not user or not user.get("partner"):
        await msg.reply("شما در حال حاضر در رابطه‌ای نیستید.")
        return

    partner_id = user["partner"]
    user["partner"] = None
    user["relationship_since"] = None
    if partner_id in data["users"]:
        data["users"][partner_id]["partner"] = None
        data["users"][partner_id]["relationship_since"] = None
    save_data(msg.chat.id, data)
    await msg.reply("💔 رابطه با موفقیت حذف شد.")

async def manual_partner(msg: types.Message):
    data = load_data(msg.chat.id)
    uid = str(msg.from_user.id)
    parts = msg.text.split()
    if len(parts) < 3:
        await msg.reply("فرمت صحیح: ثبت پارتنر @username یا ثبت اکس @username")
        return
    target_username = parts[2].lstrip("@")

    target_id = None
    for u_id, info in data["users"].items():
        if info.get("username", "").lower() == target_username.lower():
            target_id = u_id
            break
    if not target_id:
        await msg.reply("کاربری با این یوزرنیم پیدا نشد.")
        return

    if "پارتنر" in msg.text:
        data["users"].setdefault(uid, {})["partner"] = target_id
        await msg.reply(f"پارتنر جدید با موفقیت تنظیم شد ✅")
    elif "اکس" in msg.text:
        data["users"].setdefault(uid, {}).setdefault("exes", []).append(target_id)
        await msg.reply("اکس جدید با موفقیت ثبت شد ❌")

    save_data(msg.chat.id, data)
