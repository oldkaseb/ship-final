import os

# توکن ربات از متغیر محیطی
BOT_TOKEN = os.getenv('BOT_TOKEN')

# آیدی سازنده اصلی برای کنترل ربات
ADMIN_ID = int(os.getenv('ADMIN_ID')) if os.getenv('ADMIN_ID') else None

# آیدی کانال برای اجبار عضویت
CHANNEL_USERNAME = os.getenv("CHANNEL_USERNAME")  # مثل: @mychannel
CHANNEL_LINK = os.getenv("CHANNEL_LINK")  # لینک مستقیم

# نام ربات برای پیام‌های دکمه‌ها یا اعلان‌ها
BOT_NAME = "فضول گروه"

# آیدی تیم سازنده (در پیام‌های اطلاع‌رسانی استفاده می‌شود)
CREATOR_TAG = "@oldkaseb"
TEAM_NAME = "Souls"
