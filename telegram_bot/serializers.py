from rest_framework.serializers import ModelSerializer

from product.models import Product
from .models import TelegramUser

from rest_framework import serializers
from .models import TelegramUser


class TelegramUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = TelegramUser
        fields = ['telegram_id', 'username', 'name', 'phone', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


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
