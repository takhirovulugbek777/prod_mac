FROM python:3.11-slim

# Install PostgreSQL development libraries
RUN apt-get update && apt-get install -y gcc libpq-dev

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn

# Copy project files
COPY . .

# Expose port 8000 (the port the Django app is running on)
EXPOSE 8000

# Create a script to run both Django and the bot
COPY ./entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Run the application using the entrypoint script
ENTRYPOINT ["/entrypoint.sh"]
