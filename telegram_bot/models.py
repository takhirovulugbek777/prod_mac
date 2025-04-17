from django.db import models

from django.db import models
from django.core.exceptions import ValidationError


class TelegramUser(models.Model):
    telegram_id = models.BigIntegerField(unique=True)
    username = models.CharField(max_length=100, blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name or self.username or self.telegram_id}"


class Text(models.Model):
    text = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.pk and Text.objects.exists():
            raise ValidationError("Faqat bitta Text obyektiga ruxsat berilgan.")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Info - text: {self.text[:10]}"


class CreditCategory(models.Model):
    title = models.CharField(max_length=100)
    prepayment_persentage = models.IntegerField()
    qqs_persent = models.IntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title}"


class CreditPercentage(models.Model):
    month = models.IntegerField()
    persent = models.IntegerField()
    category = models.ForeignKey(CreditCategory, on_delete=models.CASCADE)

    def __str__(self):
        return f" {self.category.title} -- {self.month} -- {self.persent}"
