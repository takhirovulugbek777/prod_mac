from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext
import aiohttp
from asgiref.sync import sync_to_async

from bot.constants import BASE_URL
from bot.states import Form
from bot.keyboards.persent import category_kb
from bot.keyboards.back import back_kb
from bot.keyboards.main_kb import main_menu_kb

router = Router()


@sync_to_async
def get_category_id_by_title(title: str):
    from telegram_bot.models import CreditCategory
    category = CreditCategory.objects.get(title=title)
    return category.id, category.prepayment_persentage


@router.message(F.text == "🕒 Muddat")
async def show_category(msg: Message, state: FSMContext):
    keyboard = await category_kb()
    await msg.answer("Kredit turini tanlang:", reply_markup=keyboard)
    await state.set_state(Form.category_id)


@router.message(Form.category_id)
async def select_category(msg: Message, state: FSMContext):
    if msg.text == "🔄 Davom ettirish":
        await msg.answer("📂 Asosiy menu:", reply_markup=main_menu_kb)
        await state.clear()
        return

    try:
        category_id, percent = await get_category_id_by_title(msg.text)
        await state.update_data(category_id=category_id, percent=percent)

        await msg.answer("Iltimos, summa kiriting:", reply_markup=back_kb)
        await state.set_state(Form.amount)
    except Exception:
        await msg.answer("❌ Noto‘g‘ri kategoriya tanlandi.")


@router.message(Form.amount)
async def get_amount(msg: Message, state: FSMContext):
    if msg.text == "🔄 Davom ettirish":
        keyboard = await category_kb()
        await msg.answer("Qayta kredit turini tanlang:", reply_markup=keyboard)
        await state.set_state(Form.category_id)
        return

    try:
        amount = float(msg.text)
        data = await state.get_data()
        category_id = data['category_id']
        percent = data['percent']

        # 🔸 QQS ni olish uchun DB dan modelni olib kelamiz
        from telegram_bot.models import CreditCategory
        category = await sync_to_async(CreditCategory.objects.get)(id=category_id)
        qqs_percent = category.qqs_persent

        qqs_amount = amount * (qqs_percent / 100)
        total_with_qqs = amount + qqs_amount

        # 🔸 Asl summaga qarab oldindan to‘lov va qolgan summa hisoblaymiz
        prepayment = amount * (percent / 100)
        remaining_for_api = total_with_qqs - prepayment

        # 🔸 APIdan hisob-kitobni olib kelamiz
        api_url = f"{BASE_URL}/bot-api/category/{category_id}/?amount={remaining_for_api}"
        async with aiohttp.ClientSession() as session:
            async with session.get(api_url) as response:
                data = await response.json()

                if response.status == 200:
                    await state.update_data(
                        amount=amount,
                        calculations=data,
                        qqs_amount=int(round(qqs_amount)),
                        total_with_qqs=total_with_qqs,
                        percent=percent
                    )

                    msg_txt = (
                        f"✅ Hisob-kitob natijalari:\n\n"

                        f"📊 Oldindan to'lov ({percent}%): {int(round(prepayment))} $\n"
                        f"📊 Qolgan summa: {int(round(amount - prepayment))} $\n\n"
                        f"To'lov rejalari:\n"
                        "<pre>"
                    )

                    for calc in data["calculations"]:
                        msg_txt += f"{calc['month']} oy - {calc['payment_per_month']} $\n"
                    msg_txt += "</pre>"

                    kb = ReplyKeyboardMarkup(
                        keyboard=[
                            [KeyboardButton(text="✏️ Oldindan to‘lovni o‘zgartirish")],
                            [KeyboardButton(text="🔄 Davom ettirish"), KeyboardButton(text="🏠 Asosiy menyu")]
                        ],
                        resize_keyboard=True
                    )
                    await msg.answer(msg_txt, reply_markup=kb, parse_mode="HTML")
                    await state.set_state(Form.prepayment_amount)
                else:
                    await msg.answer("❌ Xatolik yuz berdi. Qayta urinib ko‘ring.", reply_markup=back_kb)
    except ValueError:
        await msg.answer("❌ Iltimos, raqam kiriting (masalan: 500000)", reply_markup=back_kb)


@router.message(Form.prepayment_amount)
async def edit_prepayment(msg: Message, state: FSMContext):
    if msg.text == "🔄 Davom ettirish":
        await state.set_state(Form.amount)
        await msg.answer("Iltimos, summa kiriting:", reply_markup=back_kb)
    elif msg.text == "🏠 Asosiy menyu":
        await state.clear()
        await msg.answer("📂 Asosiy menyu:", reply_markup=main_menu_kb)
    elif msg.text == "✏️ Oldindan to‘lovni o‘zgartirish":
        await state.set_state(Form.new_prepayment_amount)  # 👈 yangi state
        await msg.answer("Yangi oldindan to'lov summasini kiriting:", reply_markup=back_kb)
    else:
        await msg.answer("❌ Noto‘g‘ri tanlov! Iltimos, pastdagi tugmalardan birini tanlang.")


@router.message(Form.new_prepayment_amount)
async def handle_custom_prepayment(msg: Message, state: FSMContext):
    try:
        user_input = float(msg.text)
        data = await state.get_data()
        total_amount = data['amount']  # Kredit summasi (QQS bo‘lmasdan)
        percent = data['percent']
        qqs_amount = data.get('qqs_amount', 0)
        total_with_qqs = total_amount + qqs_amount

        min_prepayment = total_with_qqs * (percent / 100)

        # ✅ Validatsiyalar:
        if total_amount <= 0:
            await msg.answer("❌ Kredit summasi hali kiritilmagan yoki noto‘g‘ri.")
            return

        if user_input <= 0:
            await msg.answer("❌ Oldindan to‘lov 0 dan katta bo‘lishi kerak!")
            return

        if user_input < min_prepayment:
            await msg.answer(
                f"❌ Oldindan to‘lov {percent}% dan kam bo‘lmasligi kerak! "
                f"Kamida {int(min_prepayment)} $ bo‘lishi kerak."
            )
            return

        if user_input >= total_amount:
            await msg.answer(
                f"❌ Oldindan to‘lov kredit summasidan ({int(total_amount)} $) ko‘p bo‘lishi mumkin emas."
            )
            return

        # 🔹 Hisoblash
        display_remaining = total_amount - user_input  # Foydalanuvchiga ko‘rsatiladigan qolgan summa
        real_remaining = total_with_qqs - user_input  # Backend uchun haqiqiy summa (QQS bilan)

        percentages = data['calculations']['calculations']

        msg_txt = (
            f"✅ Hisob-kitob (yangi oldindan to‘lov bilan):\n\n"
            f"📊 Oldindan to‘lov: {int(user_input)} $\n"
            f"📊 Qolgan summa: {int(display_remaining)} $\n\n"
            f"To‘lov rejalari:\n"
            "<pre>"
        )

        for calc in percentages:
            total_payment = real_remaining * (1 + calc['persent'] / 100)
            per_month = total_payment / calc['month']
            msg_txt += f"{calc['month']} oy: {int(round(per_month))} $\n"
        msg_txt += "</pre>"
        await msg.answer(msg_txt, reply_markup=main_menu_kb, parse_mode="HTML")
        await state.clear()

    except ValueError:
        await msg.answer("❌ Iltimos, faqat raqam kiriting (masalan: 150000)", reply_markup=back_kb)
