import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ParseMode
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import asyncio

from config import OWNER_ID, DEBUG_MODE, LOG_FILE, BOT_NAME, TIMEZONE, NIGHTLY_SHIP_HOUR
from handlers import start, shipper, relation, profile, crash, admin, tagger, debug, stats, misc
from utils.scheduler import schedule_nightly_ship
from utils.db import ensure_data_folder

import pytz

# راه‌اندازی لاگ‌ها
logging.basicConfig(
    level=logging.DEBUG if DEBUG_MODE else logging.INFO,
    filename=LOG_FILE,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# ایجاد ربات
BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

# اطمینان از وجود پوشه data/
ensure_data_folder()

# ثبت همه هندلرها
start.register_handlers(dp)
shipper.register_handlers(dp)
relation.register_handlers(dp)
profile.register_handlers(dp)
crash.register_handlers(dp)
admin.register_handlers(dp)
tagger.register_handlers(dp)
debug.register_handlers(dp)
stats.register_handlers(dp)
misc.register_handlers(dp)

# زمان‌بندی شیپر شبانه
scheduler = AsyncIOScheduler(timezone=pytz.timezone(TIMEZONE))
schedule_nightly_ship(scheduler, bot)
scheduler.start()


# ریپورت خطا برای مالک (فقط در دیباگ)
@dp.errors_handler()
async def error_handler(update, exception):
    if DEBUG_MODE:
        try:
            await bot.send_message(OWNER_ID, f"⚠️ خطا:\n<code>{exception}</code>")
        except:
            pass
    return True


# اجرای ربات
if __name__ == '__main__':
    logging.info(f"{BOT_NAME} is starting...")
    executor.start_polling(dp, skip_updates=True)
