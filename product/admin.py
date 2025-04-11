from django.contrib import admin
from django.contrib.auth.models import Group, User

from .models import Client, Product

admin.site.unregister(Group)
admin.site.unregister(User)


class ProductInline(admin.TabularInline):  # Yoki admin.StackedInline agar boshqa ko‘rinish istasangiz
    model = Product
    extra = 1  # Yangi bo‘sh form nechta bo‘lsin
    fields = ['name', 'serial_number', 'warranty_period', 'sold_date', 'is_warranty_active']
    readonly_fields = ['is_warranty_active']


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone']
    search_fields = ['name', 'phone']
    inlines = [ProductInline]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'serial_number', 'client', 'is_warranty_active', 'sold_date']
    search_fields = ['name', 'serial_number', 'client__name', 'client__phone']
    list_filter = ['is_warranty_active', 'sold_date', 'warranty_period']
