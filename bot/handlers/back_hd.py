from aiogram import Router, F
from aiogram.types import Message
from bot.keyboards.main_kb import main_menu_kb
from aiogram.fsm.context import FSMContext

router = Router()


@router.message(F.text == "🔙 Orqaga")
async def back_to_main_menu(msg: Message, state: FSMContext):
    await state.clear()
    await msg.answer("🗂 Asosiy menu:", reply_markup=main_menu_kb)

