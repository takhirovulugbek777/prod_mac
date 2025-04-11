from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

back_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🔙 Orqaga")],

    ],
    resize_keyboard=True,
    one_time_keyboard=True
)
