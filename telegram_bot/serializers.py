from rest_framework.serializers import ModelSerializer

from product.models import Product, Client
from .models import TelegramUser

from rest_framework import serializers


class TelegramUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = TelegramUser
        fields = ['telegram_id', 'username', 'name', 'phone', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

    def create(self, validated_data):
        # Telefon raqamidan "+" belgisi va bo'sh joylarni olib tashlaymiz
        phone = validated_data.get('phone', '')
        cleaned_phone = phone.replace('+', '').replace(' ', '').strip()
        validated_data['phone'] = cleaned_phone

        # Telegram foydalanuvchisini yaratamiz
        telegram_user = super().create(validated_data)

        name = validated_data.get('name')

        if cleaned_phone:
            Client.objects.get_or_create(
                phone=cleaned_phone,
                defaults={"name": name}
            )

        return telegram_user


# serializers.py

from rest_framework import serializers
from .models import CreditCategory, CreditPercentage


class CreditPercentageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreditPercentage
        fields = ['month', 'persent']


class CreditCategorySerializer(serializers.ModelSerializer):
    credit_percentages = CreditPercentageSerializer(many=True, read_only=True)

    class Meta:
        model = CreditCategory
        fields = ['id', 'title', 'prepayment_persentage', 'credit_percentages']


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
