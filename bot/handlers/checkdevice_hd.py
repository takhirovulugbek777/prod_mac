from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
import aiohttp

from bot.constants import BASE_URL
from bot.keyboards.main_kb import main_menu_kb
from bot.keyboards.back import back_kb

router = Router()


class DeviceCheckState(StatesGroup):
    waiting_for_serial = State()


@router.message(F.text == "🔒 Kafolat")
async def kafolat_handler(message: Message, state: FSMContext):
    """Handle the Kafolat button press and ask for serial number"""
    await message.answer(
        "Mahsulot serial raqamini kiriting:",
        reply_markup=back_kb
    )
    await state.set_state(DeviceCheckState.waiting_for_serial)


@router.message(DeviceCheckState.waiting_for_serial)
async def process_serial_number(message: Message, state: FSMContext):
    """Process the serial number input from user"""
    if message.text == "🔙 Orqaga":
        await message.answer("🗂 Asosiy menu:", reply_markup=main_menu_kb)
        await state.clear()
        return

    serial_number = message.text.strip()

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(BASE_URL + f'/bot-api/products/{serial_number}/') as response:
                if response.status == 200:
                    data = await response.json()

                    reply_text = f"""
🔍 Mahsulot ma'lumotlari:
📦 Nomi: {data.get('name', "Noma'lum")}
📅 Sotilgan sana: {data.get('sold_date', "Noma'lum")}
📜 Serial raqam: {data.get('serial_number', "Noma'lum")}
✅ Kafolat holati: {'Aktiv' if data.get('is_warranty_active') else 'Muddati o‘tkazilgan'}
📆 Kafolat muddati: {data.get('warranty_period', "Noma'lum")} oy
                    """

                    await message.answer(reply_text, reply_markup=back_kb)
                elif response.status == 404:
                    await message.answer(
                        "❌ Mahsulot topilmadi. Iltimos, serial raqamini tekshiring.",
                        reply_markup=back_kb
                    )
                else:
                    print(f"API xatosi! Status kodi: {response.status}")
                    await message.answer(
                        "❌ Xatolik yuz berdi. Keyinroq qayta urinib ko'ring.",
                        reply_markup=back_kb
                    )

    except Exception as e:
        await message.answer(
            "❌ Server bilan bog'lanishda xatolik yuz berdi. Keyinroq urinib ko'ring.\n"
            f"{str(e)}",
            reply_markup=back_kb
        )
