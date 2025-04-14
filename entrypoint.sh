#!/bin/bash

echo "Collecting static files..."
python manage.py collectstatic --noinput
# Django'ni Gunicorn orqali foregroundda ishga tushiramiz
echo "Starting Django with Gunicorn..."
gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 3 &

# Django yuklanishini kutamiz
echo "Waiting for Django to start up..."
sleep 5

# Telegram botni ishga tushiramiz
echo "Starting Telegram bot..."
python run_bot.py
