# config.py - تنظیم متغیرهای محیطی ربات

import os

# توکن ربات از محیط Railway
BOT_TOKEN = os.getenv("BOT_TOKEN")

# آیدی عددی سازنده اصلی (مثلاً 7662192190)
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))

# آیدی کانالی که کاربران باید عضو باشند (اختیاری)
CHANNEL_ID = os.getenv("CHANNEL_ID", "")

# تست رایگان اولیه برای هر گروه چند روزه است؟
FREE_TRIAL_DAYS = int(os.getenv("FREE_TRIAL_DAYS", "7"))

# مسیر پوشه ذخیره دیتای گروه‌ها
DATA_FOLDER = "data"

# قیمت شارژ ماهیانه (توضیحی صرفاً برای پیام استارت)
MONTHLY_PRICE = "۵۰ هزار تومان"

# آیدی تلگرام مالک برای دکمه تماس
OWNER_USERNAME = "@oldkaseb"
