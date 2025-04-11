from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from asgiref.sync import sync_to_async

from telegram_bot.models import CreditCategory


@sync_to_async
def category_kb():
    categories = CreditCategory.objects.all()
    keyboard = []
    for category in categories:
        keyboard.append([KeyboardButton(text=category.title)])
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
        one_time_keyboard=True
    )
