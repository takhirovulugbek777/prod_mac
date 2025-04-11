# import asyncio
# import os
# from dotenv import load_dotenv
# from aiogram import Bot, Dispatcher
#
# from .handlers import register, info, back_hd, persent_hd, checkdevice_hd
#
# load_dotenv()  # bu .env faylini yuklaydi
# BASE_URL = os.getenv("BASE_URL")
#
# async def main():
#     bot = Bot(token=os.getenv("BOT_TOKEN"))  # <-- bu yerda stringda yoziladi
#     dp = Dispatcher()
#
#     dp.include_router(register.router)
#     dp.include_router(info.router)
#     dp.include_router(back_hd.router)
#     dp.include_router(persent_hd.router)
#     dp.include_router(checkdevice_hd.router)
#
#     await dp.start_polling(bot)
#
#
# if __name__ == "__main__":
#     asyncio.run(main())
import asyncio
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher

from .handlers import register, info, back_hd, persent_hd, checkdevice_hd
import asyncio
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher

# Import constants from the dedicated constants file instead
from .constants import BOT_TOKEN
from .handlers import register, info, back_hd, persent_hd, checkdevice_hd


# No need to load_dotenv() or define BASE_URL here since it's in constants.py

async def main():
    print("Starting Telegram bot...")
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    dp.include_router(register.router)
    dp.include_router(info.router)
    dp.include_router(back_hd.router)
    dp.include_router(persent_hd.router)
    dp.include_router(checkdevice_hd.router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
