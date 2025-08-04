import os
from datetime import timedelta

# آیدی عددی مالک اصلی ربات (در Railway تنظیم میشه)
OWNER_ID = int(os.getenv("OWNER_ID", "1234567890"))  # این مقدار باید در Railway تعریف بشه

# منطقه زمانی ایران
TIMEZONE = "Asia/Tehran"

# ساعت اجرای شیپر شبانه (ساعت ۹ شب ایران)
NIGHTLY_SHIP_HOUR = 21  # ساعت ۲۱ به وقت ایران

# مسیر پوشه ذخیره دیتای ایزوله گروه‌ها
DATA_FOLDER = "data"

# مدت تست رایگان گروه‌ها (به روز)
FREE_TRIAL_DAYS = 7

# هشدار قبل از اتمام اعتبار (۲ روز مانده)
DAYS_BEFORE_EXPIRY_WARNING = 2

# پلن‌های شارژ به روز
PLANS = {
    "1": timedelta(days=30),
    "2": timedelta(days=60),
    "3": timedelta(days=90),
    "6": timedelta(days=180),
    "∞": timedelta(days=365 * 100),  # عملاً نامحدود
}

# آیدی فروشنده‌ها (در طول پروژه قابل اضافه‌کردن)
SELLERS = []  # به‌صورت [123456, 987654] اضافه می‌شن

# نام فایل لاگ‌ها
LOG_FILE = "logs.txt"

# فعال‌سازی حالت دیباگ (True = نمایش خطاها برای مالک)
DEBUG_MODE = True

# نام ربات برای استفاده در پیام‌ها
BOT_NAME = "فضول گروه"
