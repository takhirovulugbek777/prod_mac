from aiogram import Router, F
from aiogram.types import Message

from asgiref.sync import sync_to_async
from telegram_bot.models import Text
from bot.keyboards.back import back_kb

router = Router()


@sync_to_async
def get_info_text():
    return Text.objects.first().text if Text.objects.exists() else "Ma'lumot topilmadi."


@router.message(F.text == "🔍 Info")
async def info_handler(msg: Message):
    info_text = await get_info_text()
    await msg.answer(f"ℹ️ {info_text}", reply_markup=back_kb, parse_mode="HTML")
