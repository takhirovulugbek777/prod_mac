import os
import django
import asyncio

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

# Import and run the bot
from bot.bot import main

if __name__ == '__main__':
    asyncio.run(main())
