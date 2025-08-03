# config.py

import os

# گرفتن توکن ربات از متغیر محیطی
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("❌ متغیر محیطی BOT_TOKEN یافت نشد!")

# تعریف لیست ادمین‌ها
ADMINS = [
    7662192190  # آیدی عددی شما
]

# اگر خواستی متغیرهای محیطی دیگر رو هم اضافه کنیم (مثلاً برای شارژ یا API یا کانال‌ها)، فقط بگو.
