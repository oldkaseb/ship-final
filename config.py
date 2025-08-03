import os

# ✅ توکن ربات از محیط Railway
TOKEN = os.getenv("BOT_TOKEN")

# ✅ لیست ادمین‌های اصلی برای مدیریت ربات (می‌تواند چند نفر باشد)
ADMINS = os.getenv("ADMIN_ID", "").split(",")  # به‌صورت لیست ['123456', '654321']

# ✅ کانال اجبار عضویت
FORCE_CHANNEL = os.getenv("CHANNEL_USERNAME", "")  # مثال: @mychannel

# ✅ آیدی عددی کانال برای بررسی عضویت (با استفاده از ID کانال عمومی)
FORCE_CHANNEL_ID = int(os.getenv("CHANNEL_ID", "0"))

# ✅ مسیر ذخیره‌سازی دیتا برای هر گروه
DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)
