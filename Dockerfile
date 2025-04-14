FROM python:3.11-slim

# Kerakli tizim kutubxonalarini o‘rnatish
RUN apt-get update && apt-get install -y gcc libpq-dev

# Muhit o‘zgaruvchilari
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Ishchi papkani sozlash
WORKDIR /app

# Kutubxonalarni o‘rnatish
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn

# Kod fayllarini nusxalash
COPY . .

# Portni ochish (endi 8000-da ishlaydi)
EXPOSE 8000

# Kirish faylini qo‘shish
COPY ./entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Kirish fayli orqali ishga tushirish
ENTRYPOINT ["/entrypoint.sh"]
