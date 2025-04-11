#!/bin/bash

# Update the database settings to use the Docker service name
sed -i "s/POSTGRES_HOST=localhost/POSTGRES_HOST=db/g" .env

# Start Django with Gunicorn in the background
echo "Starting Django with Gunicorn..."
gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 3 --daemon

# Wait for Django to start up
echo "Waiting for Django to start up..."
sleep 5

# Start the bot
echo "Starting Telegram bot..."
python run_bot.py

# Keep the container running
tail -f /dev/null
