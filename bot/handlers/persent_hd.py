from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
import aiohttp
from asgiref.sync import sync_to_async

from bot.constants import BASE_URL
from bot.keyboards.persent import category_kb
from bot.keyboards.back import back_kb
from bot.keyboards.main_kb import main_menu_kb

router = Router()


class Form(StatesGroup):
    category_id = State()
    amount = State()


@router.message(F.text == "🕒 Muddat")
async def show_category(msg: Message, state: FSMContext):
    category_keyboard = await category_kb()
    await msg.answer("Kredit turini tanlang: ", reply_markup=category_keyboard)
    await state.set_state(Form.category_id)


@router.message(Form.category_id)
async def select_category(msg: Message, state: FSMContext):
    if msg.text == "🔙 Orqaga":
        await msg.answer("🗂 Asosiy menu:", reply_markup=main_menu_kb)
        await state.clear()
        return

    selected_category_title = msg.text
    try:
        category_id = await get_category_id_by_title(selected_category_title)
        await state.update_data(category_id=category_id)

        await msg.answer("Iltimos, summa kiriting:", reply_markup=back_kb)
        await state.set_state(Form.amount)
    except Exception:
        await msg.answer("❌ Noto‘g‘ri kategoriya tanlandi.")


async def get_category_id_by_title(title: str):
    from telegram_bot.models import CreditCategory
    category = await sync_to_async(CreditCategory.objects.get)(title=title)
    return category.id


@router.message(Form.amount)
async def get_amount(msg: Message, state: FSMContext):
    if msg.text == "🔙 Orqaga":
        # Orqaga qaytish - yana category tanlansin
        category_keyboard = await category_kb()
        await msg.answer("Qayta kredit turini tanlang:", reply_markup=category_keyboard)
        await state.set_state(Form.category_id)
        return

    elif msg.text == "🏠 Asosiy menyu":
        # State tozalansin va asosiy menyuga qaytsin
        await state.clear()
        await msg.answer("🗂 Asosiy menyu:", reply_markup=main_menu_kb)
        return

    # Add a check to ensure we're in the right state
    current_state = await state.get_state()
    if current_state != Form.amount:
        await msg.answer("🗂 Asosiy menu:", reply_markup=main_menu_kb)
        await state.clear()
        return

    try:
        user_data = await state.get_data()
        category_id = user_data['category_id']
        amount = float(msg.text)

        api_url = (BASE_URL + f"/bot-api/category/{category_id}/?amount={amount}")
        async with aiohttp.ClientSession() as session:
            async with session.get(api_url) as response:
                data = await response.json()

                if response.status == 200:
                    prepayment_amount = data["prepayment_amount"]
                    remaining_amount = data["remaining_amount"]
                    calculations = data["calculations"]

                    response_message = f"✅ Hisob-kitob natijalari:\n\n"
                    response_message += f"📊 Oldindan to'lov: {prepayment_amount} $\n"
                    response_message += f"📊 Qolgan summa: {remaining_amount} $\n\n"
                    response_message += "📅 To'lov rejalari:\n"
                    for calc in calculations:
                        response_message += f"{calc['month']} oy: {calc['payment_per_month']} $\n"

                    # After showing results, clear the state and return to main menu
                    await msg.answer(response_message, reply_markup=main_menu_kb)
                    await state.clear()
                else:
                    await msg.answer("❌ Xatolik yuz berdi. Iltimos, qayta urinib ko'ring.", reply_markup=back_kb)
    except ValueError:
        await msg.answer("❌ Iltimos, raqam kiriting (masalan: 500000)", reply_markup=back_kb)
