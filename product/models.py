from datetime import timedelta, date
from django.db import models


class Client(models.Model):
    name = models.CharField(max_length=255, verbose_name="Client Name")
    phone = models.CharField(
        max_length=15,
        unique=True,
        verbose_name="Phone Number",
        help_text="Enter the phone number (up to 15 digits)."
    )

    def __str__(self):
        return f"{self.name} - {self.phone}"


class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name="Product Name")
    is_warranty_active = models.BooleanField(
        default=True,
        verbose_name="Is Warranty Active",
        help_text="Indicates if the product warranty is still valid."
    )
    warranty_period = models.PositiveIntegerField(
        verbose_name="Warranty Period (Months)",
        help_text="Warranty duration in months (must be positive)."
    )
    sold_date = models.DateField(
        default=date.today,
        verbose_name="Date Sold",
        help_text="Date when the product was sold."
    )
    serial_number = models.CharField(
        max_length=50,  # Optimal uzunlik tanlangan
        unique=True,
        verbose_name="Serial Number",
        help_text="Unique identifier for the product."
    )
    client = models.ForeignKey(
        Client,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='products'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Last Updated")

    def save(self, *args, **kwargs):
        self.is_warranty_active = self.is_warranty_valid()
        super().save(*args, **kwargs)

    def is_warranty_valid(self):
        warranty_end_date = self.get_warranty_end_date()
        return date.today() <= warranty_end_date

    def get_warranty_end_date(self):
        return self.sold_date + timedelta(days=self.warranty_period * 30)

    def __str__(self):
        return f"{self.name} - {self.serial_number}"

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
        ordering = ['-created_at']
