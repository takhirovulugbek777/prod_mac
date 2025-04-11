import aiohttp
from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from bot.constants import BASE_URL
from bot.states import RegisterState
from bot.keyboards.phone import contact_kb, register
from bot.keyboards.main_kb import main_menu_kb
from telegram_bot.models import TelegramUser
from asgiref.sync import sync_to_async

router = Router()


@sync_to_async
def check_user_registered(telegram_id: int) -> bool:
    return TelegramUser.objects.filter(telegram_id=telegram_id).exists()


@router.message(CommandStart())
async def start_cmd(msg: Message, state: FSMContext):
    user_registered = await check_user_registered(msg.from_user.id)

    if user_registered:
        await msg.answer(
            "🗂 Asosiy menu:",
            reply_markup=main_menu_kb  # Main menu with Info, Muddat, Kafolat options
        )
    else:
        await msg.answer("Ismingizni kiriting:")
        await state.set_state(RegisterState.name)


@router.message(RegisterState.name)
async def get_name(msg: Message, state: FSMContext):
    await state.update_data(name=msg.text)
    await msg.answer("Telefon raqamingizni kontakt sifatida yuboring:", reply_markup=contact_kb)
    await state.set_state(RegisterState.phone)


@router.message(RegisterState.phone, F.contact)
async def get_phone(msg: Message, state: FSMContext):
    user_data = await state.get_data()
    phone = msg.contact.phone_number

    payload = {
        "telegram_id": msg.from_user.id,
        "username": msg.from_user.username,
        "name": user_data.get("name"),
        "phone": phone
    }

    async with aiohttp.ClientSession() as session:
        async with session.post((BASE_URL + "/bot-api/usercreate/"), json=payload) as response:
            print("STATUS CODE:", response.status)
            text = await response.text()
            print("RESPONSE TEXT:", text)
            if response.status == 201:
                await msg.answer("✅ Muvaffaqiyatli ro‘yxatdan o‘tdingiz!", reply_markup=main_menu_kb)
            else:
                await msg.answer(f"❌ Xatolik: {text}")

    await state.clear()


@router.message(RegisterState.phone)
async def phone_error(msg: Message):
    await msg.answer(
        "❌ Iltimos, telefon raqamingizni qo‘lda emas, *kontakt sifatida* yuboring.",
        reply_markup=contact_kb,
        parse_mode="Markdown"
    )
