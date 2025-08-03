# loader.py - بارگذاری اولیه Bot و Dispatcher

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from config import BOT_TOKEN

# حافظه موقت برای ذخیره داده‌ها (مثلاً برای مکالمات مرحله‌ای)
storage = MemoryStorage()

# ساخت نمونه‌های Bot و Dispatcher
bot = Bot(token=BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher(bot, storage=storage)
