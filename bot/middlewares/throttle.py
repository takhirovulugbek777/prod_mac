# middlewares/throttle.py
from aiogram import BaseMiddleware
from aiogram.types import Message
from datetime import datetime, timedelta

# Global dict: har bir foydalanuvchining oxirgi xabar vaqti
user_last_message = {}


class ThrottleMiddleware(BaseMiddleware):
    def __init__(self, limit_seconds: int = 5):
        self.limit = timedelta(seconds=limit_seconds)
        super().__init__()

    async def __call__(self, handler, event, data):
        if isinstance(event, Message):
            now = datetime.now()
            user_id = event.from_user.id

            if user_id in user_last_message and now - user_last_message[user_id] < self.limit:
                await event.answer("⛔ Juda tez yozayapsiz. Biroz kuting.")
                return

            user_last_message[user_id] = now

        return await handler(event, data)
