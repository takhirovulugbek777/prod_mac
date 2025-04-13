from bot.middlewares.throttle import ThrottleMiddleware
import asyncio
from aiogram import Bot, Dispatcher

from .constants import BOT_TOKEN
from .handlers import register, info, back_hd, persent_hd, checkdevice_hd


# No need to load_dotenv() or define BASE_URL here since it's in constants.py

async def main():
    print("Starting Telegram bot...")
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    dp.message.middleware(ThrottleMiddleware(max_messages=3, per_seconds=1))

    dp.include_router(register.router)
    dp.include_router(info.router)
    dp.include_router(back_hd.router)
    dp.include_router(persent_hd.router)
    dp.include_router(checkdevice_hd.router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
