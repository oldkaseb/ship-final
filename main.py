import asyncio
from loader import dp, bot
from handlers.start import run
from aiogram import executor

# ثبت تمام هندلرها
run()

async def on_startup(dispatcher):
    print("ربات با موفقیت راه‌اندازی شد.")

async def main():
    await on_startup(dp)
    await dp.start_polling()

if __name__ == "__main__":
    asyncio.run(main())
