from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from telegram_bot.models import CreditCategory
from asgiref.sync import sync_to_async


@sync_to_async
def category_kb():
    categories = CreditCategory.objects.all()
    buttons = [[KeyboardButton(text=cat.title)] for cat in categories]
    buttons.append([KeyboardButton(text="🔙 Orqaga")])
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)


prepayment_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="✏️ Boshlangʻich toʻlovni o‘zgartirish")],
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)
