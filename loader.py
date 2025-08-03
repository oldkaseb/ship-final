# loader.py - فایل لودر برای ساخت Bot و Dispatcher

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from config import TOKEN

bot = Bot(token=TOKEN, parse_mode="HTML")
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
