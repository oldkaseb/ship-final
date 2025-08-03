# config.py

import os
from dotenv import load_dotenv

# بارگذاری متغیرها از .env (برای لوکال)
load_dotenv()

# توکن ربات از محیط (Railway یا .env)
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("❌ متغیر محیطی BOT_TOKEN یافت نشد! آن را در Railway یا فایل .env تعریف کنید.")

# سایر متغیرهای قابل افزودن در آینده:
# ADMIN_ID = os.getenv("ADMIN_ID")
# CHANNEL_ID = os.getenv("CHANNEL_ID")
