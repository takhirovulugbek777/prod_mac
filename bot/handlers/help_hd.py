from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from bot.keyboards.main_kb import main_menu_kb

router = Router()


# @router.message(Command("help"))  # This replaces CommandHelp()
# async def help_cmd(msg: Message):
#     help_text = (
#         "🆘 *Yordam bo'limi*\n\n"
#         "Ushbu botni qanday ishlatishni bilish uchun quyidagi komandalarni kiriting:\n\n"
#         "/start - Botni boshlash\n"
#         "/help - Yordam\n"
#         "Asosiy menyuda mavjud bo‘lgan funksiyalar haqida ma'lumot olish.\n\n"
#         "Telefon raqamingizni kiriting, va boshqa kerakli ma'lumotlarni olish uchun botni davom ettiring."
#     )
#
#     await msg.answer(help_text, reply_markup=main_menu_kb, parse_mode="Markdown")
@router.message(Command("help"))
async def help_cmd(msg: Message):
    help_text = (
        "🆘 <b>Yordam bo‘limi</b>\n\n"
        "Assalomu alaykum! Ushbu bot orqali siz qurilmangiz haqida ma’lumot olishingiz mumkin.\n\n"
        "<b>📌 Asosiy buyruqlar:</b>\n"
        "/start - Botni ishga tushurish\n"
        "/help - Yordam va qo‘llanma\n\n"
        "📱 Telefon raqamingizni yuborish orqali xizmatdan to‘liq foydalanishingiz mumkin.\n\n"
        "🌐 Bot veb-sayti: <a href='https://checkdevice.uz'>checkdevice.uz</a>\n\n"
        "👨‍💻 Dasturchi: @takhirov_U\n"
        "📞 Bog‘lanish: +998938802032\n\n"
        "📣 Telegram kanal: <a href='https://t.me/macshop_uz'>@macshop_uz</a>\n"
        "🛠 Admin: <a href='https://t.me/macshop_admin'>@macshop_admin</a>\n\n"
        "<i>Yordam kerak bo‘lsa, bemalol murojaat qiling. Hurmat bilan, Takhirov.</i>"
    )
    await msg.answer(help_text, parse_mode="HTML")
