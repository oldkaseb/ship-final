# handlers/info.py
from aiogram import types
from utils.db import load_group_data

def format_user_info(user):
    return (
        f"اسم: {user.get('name', '-')}, "
        f"سن: {user.get('age', '-')}, "
        f"قد: {user.get('height', '-')}, "
        f"شهر: {user.get('city', '-')}, "
        f"جنسیت: {user.get('gender', '-')}, "
        f"تولد: {user.get('birthday', '-')}, "
        f"وضعیت: {user.get('status', '-')}"
    )

async def handle_whoami(msg: types.Message):
    if msg.chat.type == "private":
        return

    data = load_group_data(msg.chat.id)
    user = data["users"].get(str(msg.from_user.id))

    if not user:
        await msg.reply("❗️شما هنوز اطلاعاتی ثبت نکرده‌اید.")
        return

    crushes = data.get("crushes", {}).get(str(msg.from_user.id), [])
    couple = user.get("couple")
    ex = user.get("ex")
    birthday = user.get("birthday", "-")

    text = f"📋 اطلاعات شما:\n{format_user_info(user)}\n"
    text += f"\n❤️ رل فعلی: {couple if couple else '-'}"
    text += f"\n💔 اکس: {ex if ex else '-'}"
    text += f"\n🔥 لیست کراش‌ها: {', '.join(crushes) if crushes else '-'}"

    await msg.reply(text)

async def handle_list_crushes(msg: types.Message):
    if msg.chat.type == "private":
        return

    data = load_group_data(msg.chat.id)
    crushes = data.get("crushes", {}).get(str(msg.from_user.id), [])

    if not crushes:
        await msg.reply("😅 شما هنوز هیچ کراشی ثبت نکردید.")
        return

    text = "📍 لیست کراش‌های شما:\n"
    for i, cid in enumerate(crushes, 1):
        text += f"{i}. {cid}\n"
    await msg.reply(text)

async def handle_list_couples(msg: types.Message):
    if msg.chat.type == "private":
        return

    data = load_group_data(msg.chat.id)
    couples = data.get("couples", [])

    if not couples:
        await msg.reply("❌ هنوز هیچ کاپلی در این گروه ثبت نشده.")
        return

    text = "💑 لیست کاپل‌های این گروه:\n"
    for i, (u1, u2) in enumerate(couples, 1):
        text += f"{i}. {u1} ❤️ {u2}\n"
    await msg.reply(text)

async def handle_list_admins(msg: types.Message):
    if msg.chat.type == "private":
        return

    data = load_group_data(msg.chat.id)
    admins = data.get("settings", {}).get("admins", [])

    if not admins:
        await msg.reply("🔸 هیچ مدیری برای این گروه تعریف نشده.")
        return

    text = "👮‍♀️ لیست مدیران:\n"
    for i, admin_id in enumerate(admins, 1):
        text += f"{i}. {admin_id}\n"
    await msg.reply(text)

async def handle_last_night_ship(msg: types.Message):
    if msg.chat.type == "private":
        return

    data = load_group_data(msg.chat.id)
    last_ship = data.get("settings", {}).get("last_night_ship")

    if last_ship:
        await msg.reply(f"🕯 شیپ دیشب: {last_ship}")
    else:
        await msg.reply("❌ شیپ دیشب هنوز ثبت نشده.")
