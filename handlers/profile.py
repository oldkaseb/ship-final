from aiogram import types, Dispatcher
from utils.db import load_group_data, save_group_data, get_user_profile
import re
from datetime import datetime
from config import DEBUG_MODE

# دریافت اطلاعات و ذخیره مشخصات از طریق ریپلای
async def set_profile(message: types.Message):
    if message.chat.type not in ["group", "supergroup"]:
        return  # فقط در گروه

    if not message.reply_to_message:
        await message.reply("👀 باید روی پیام طرف ریپلای بزنی که مشخصات براش ثبت شه!")
        return

    group_id = message.chat.id
    target = message.reply_to_message.from_user
    text = message.text

    # استخراج مقادیر از متن
    name = extract_field(text, "اسم")
    age = extract_field(text, "سن")
    city = extract_field(text, "شهر")
    height = extract_field(text, "قد")

    if not any([name, age, city, height]):
        await message.reply("📌 لطفاً مشخصات رو با فرمت درست وارد کن. مثل:\nاسم: علی | سن: ۲۰ | شهر: تهران | قد: ۱۷۵")
        return

    data = load_group_data(group_id)
    profile = get_user_profile(data, target.id)

    if name:
        profile["name"] = name
    if age:
        if age.isdigit():
            profile["age"] = int(age)
        else:
            await message.reply("🔢 سن باید عدد باشه!")
            return
    if city:
        profile["city"] = city
    if height:
        if height.isdigit():
            profile["height"] = int(height)
        else:
            await message.reply("📏 قد باید عدد باشه!")
            return

    profile["last_updated"] = datetime.now().isoformat()
    save_group_data(group_id, data)

    await message.reply(f"✅ مشخصات {target.full_name} با موفقیت ذخیره شد 😎")


# تنظیم جنسیت با پیام مستقیم
async def set_gender(message: types.Message):
    if message.chat.type not in ["group", "supergroup"]:
        return

    group_id = message.chat.id
    user_id = message.from_user.id
    text = message.text.strip()

    data = load_group_data(group_id)
    profile = get_user_profile(data, user_id)

    if "پسرم" in text:
        profile["gender"] = "male"
        gender_text = "🤵 شما پسر ثبت شدی!"
    elif "دخترم" in text:
        profile["gender"] = "female"
        gender_text = "👸 شما دختر ثبت شدی!"
    else:
        return

    profile["last_updated"] = datetime.now().isoformat()
    save_group_data(group_id, data)

    await message.reply(f"{gender_text} ✅")


# استخراج فیلد از متن
def extract_field(text: str, key: str):
    match = re.search(fr"{key}[:：]?\s*([\u0600-\u06FFa-zA-Z0-9]+)", text)
    if match:
        return match.group(1)
    return None


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(set_profile, lambda m: any(k in m.text for k in ["اسم", "سن", "شهر", "قد"]), content_types=types.ContentType.TEXT)
    dp.register_message_handler(set_gender, lambda m: "پسرم" in m.text or "دخترم" in m.text, content_types=types.ContentType.TEXT)
