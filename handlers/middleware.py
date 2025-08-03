# middleware.py - کنترل اعتبار گروه‌ها و جلوگیری از فعالیت در گروه منقضی

from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware
from utils.db import load_group_data, save_group_data
from datetime import datetime

class AccessControlMiddleware(BaseMiddleware):
    async def on_pre_process_message(self, message: types.Message, data: dict):
        # فقط پیام‌های گروهی را بررسی کن
        if message.chat.type == "private":
            return

        chat_id = str(message.chat.id)
        group_data = load_group_data(chat_id)

        # اگر نصب نشده، نصب را فعال کن با تست رایگان 7 روزه
        if not group_data.get("installed"):
            group_data["installed"] = True
            group_data["owner_id"] = message.from_user.id
            expire_date = datetime.now().timestamp() + 7 * 24 * 60 * 60
            group_data["expiration"] = expire_date
            save_group_data(chat_id, group_data)
            await message.answer("✅ ربات با موفقیت نصب شد و تست رایگان 7 روزه فعال گردید.")
            return

        # بررسی انقضا
        if group_data.get("expiration"):
            expire_time = float(group_data["expiration"])
            now = datetime.now().timestamp()
            remaining = expire_time - now
            if remaining <= 0:
                await message.answer("⚠️ مدت زمان تست یا شارژ این گروه به پایان رسیده. برای تمدید با مالک ربات در تماس باشید.")
                return await message.bot.leave_chat(message.chat.id)
            elif remaining < 2 * 24 * 60 * 60:  # هشدار ۲ روز مانده
                try:
                    await message.bot.send_message(
                        group_data.get("owner_id"),
                        f"⏳ فقط دو روز تا پایان اعتبار گروه {message.chat.title} باقی مانده است. برای تمدید اقدام کنید."
                    )
                except:
                    pass
