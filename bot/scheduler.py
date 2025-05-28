from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram import Bot
from aiogram.types import BufferedInputFile
from datetime import datetime
from pytz import timezone
from io import BytesIO
import os
import subprocess

from .constants import BOT_TOKEN


async def send_db_backup():
    print("📦 Starting DB full SQL backup...")

    # Fayl nomi
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = f"full_backup_{timestamp}.sql"

    # Postgres ulanish parametrlari
    db_name = os.getenv("POSTGRES_DB")
    db_user = os.getenv("POSTGRES_USER")
    db_password = os.getenv("POSTGRES_PASSWORD")
    db_host = os.getenv("POSTGRES_HOST")
    db_port = os.getenv("POSTGRES_PORT")

    # Parolni o‘zgaruvchi sifatida beramiz
    env = os.environ.copy()
    env["PGPASSWORD"] = db_password

    # 🔁 FULL BACKUP SQL (plain SQL) — restore qilish oson bo‘ladi
    command = [
        "pg_dump",
        "-h", db_host,
        "-p", db_port,
        "-U", db_user,
        "-d", db_name,
        "-F", "p",  # Plain format (.sql) — eng qulay restore uchun
        "--no-owner",  # Optional: tiklashda egasi kerak bo‘lmaydi
        "--no-privileges"  # Optional: GRANT/REVOKE lar kerakmas
    ]

    try:
        result = subprocess.run(command, env=env, capture_output=True)

        if result.returncode != 0:
            print("❌ Backup failed:", result.stderr.decode())
            return

        file_bytes = BytesIO(result.stdout)
        file_bytes.name = file_name

        bot = Bot(token=BOT_TOKEN)
        await bot.send_document(
            chat_id="-1002547208302",
            document=BufferedInputFile(file_bytes.read(), filename=file_name),
            caption=f"📦 {db_name} bazasining to‘liq SQL backup fayli\n🕒 {timestamp}"
        )
        await bot.session.close()

        print("✅ Backup sent and done.")

    except Exception as e:
        print(f"❌ Backup error: {e}")


def start_scheduler():
    scheduler = AsyncIOScheduler()
    tz = timezone("Asia/Tashkent")
    scheduler.add_job(send_db_backup, 'cron', hour=18, minute=29, timezone=tz)
    scheduler.start()
