from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

contact_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📞 Kontakt ulashish", request_contact=True)]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

register = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="ro'yhatdan o'tish")]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)
