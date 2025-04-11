from django.contrib import admin

from telegram_bot.models import TelegramUser, Text

# Register your mo
admin.site.register([TelegramUser, Text])

from django.contrib import admin
from .models import CreditCategory, CreditPercentage


class CreditPercentageInline(admin.TabularInline):
    model = CreditPercentage
    extra = 1


class CreditCategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'prepayment_persentage', 'updated_at', 'created_at')
    inlines = [CreditPercentageInline]



admin.site.register(CreditCategory, CreditCategoryAdmin)
