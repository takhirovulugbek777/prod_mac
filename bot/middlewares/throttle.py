from aiogram import BaseMiddleware
from aiogram.types import Message
from datetime import datetime, timedelta
from collections import defaultdict, deque


class ThrottleMiddleware(BaseMiddleware):
    def __init__(self, max_messages: int = 3, per_seconds: int = 1):
        self.max_messages = max_messages
        self.per_seconds = per_seconds
        self.user_messages = defaultdict(deque)  # har bir user uchun vaqtlar ro'yxati

    async def __call__(self, handler, event, data):
        if isinstance(event, Message):
            now = datetime.now()
            user_id = event.from_user.id

            # foydalanuvchining so'nggi xabar vaqtlarini olib, eski vaqtlarni tozalaymiz
            timestamps = self.user_messages[user_id]
            while timestamps and (now - timestamps[0]).total_seconds() > self.per_seconds:
                timestamps.popleft()

            if len(timestamps) >= self.max_messages:
                await event.answer("⛔ Juda ko‘p xabar yubordingiz. Iltimos, sekinroq yozing.")
                return

            timestamps.append(now)

        return await handler(event, data)
