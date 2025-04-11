from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_menu_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🔍 Info"),
            KeyboardButton(text="🕒 Muddat")
        ],
        [
            KeyboardButton(text="🔒 Kafolat")
        ]
    ],
    resize_keyboard=True,  # Automatically resizes the keyboard to fit screen
    one_time_keyboard=True  # Keyboard disappears after the user clicks a button
)
