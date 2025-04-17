from bot.middlewares.throttle import ThrottleMiddleware
import asyncio
from aiogram import Bot, Dispatcher

from bot.scheduler import start_scheduler
from .constants import BOT_TOKEN
from .handlers import register, info, back_hd, persent_hd, checkdevice_hd, help_hd
from aiogram.types import BotCommand


async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="/start", description="Botni boshlash"),
        BotCommand(command="/help", description="Yordam"),
    ]
    await bot.set_my_commands(commands)


async def main():
    print("Starting Telegram bot...")
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    await set_commands(bot)

    dp.message.middleware(ThrottleMiddleware(max_messages=3, per_seconds=1))

    dp.include_router(register.router)
    dp.include_router(help_hd.router)
    dp.include_router(info.router)
    dp.include_router(back_hd.router)
    dp.include_router(persent_hd.router)
    dp.include_router(checkdevice_hd.router)

    start_scheduler()

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
