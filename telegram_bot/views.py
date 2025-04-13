from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import CreditCategory, CreditPercentage

from .models import TelegramUser
from .serializers import TelegramUserSerializer
from product.models import Product
from telegram_bot.models import TelegramUser
from telegram_bot.serializers import TelegramUserSerializer, ProductSerializer


class ProductDetailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, serial_number):
        try:
            product = Product.objects.get(serial_number=serial_number)
            serializer = ProductSerializer(product)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Product.DoesNotExist:
            return Response({"error": "Mahsulot topilmadi"}, status=status.HTTP_404_NOT_FOUND)


class TelegramUserCreateApiView(ListCreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = TelegramUserSerializer
    queryset = TelegramUser.objects.all()


# views.py

class CreditCalculationAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, cat_pk, *args, **kwargs):
        try:
            input_amount = float(request.query_params.get('amount', 0))

            if input_amount <= 0:
                return Response({"error": "Input amount must be greater than zero."},
                                status=status.HTTP_400_BAD_REQUEST)

            credit_category = CreditCategory.objects.get(id=cat_pk)
            prepayment_amount = input_amount * (credit_category.prepayment_persentage / 100)
            remaining_amount = input_amount - prepayment_amount

            credit_percentages = CreditPercentage.objects.filter(category=credit_category)

            result = []
            for credit_percentage in credit_percentages:
                calculated_amount = remaining_amount * (1 + (credit_percentage.persent / 100))
                monthly_payment = calculated_amount / credit_percentage.month
                result.append({
                    'month': credit_percentage.month,
                    'persent': credit_percentage.persent,
                    'payment_per_month': int(round(monthly_payment))
                })

            return Response({
                "prepayment_amount": int(round(prepayment_amount)),
                "remaining_amount": int(round(remaining_amount)),
                "calculations": result
            }, status=status.HTTP_200_OK)
        except CreditCategory.DoesNotExist:
            return Response({"error": "Credit category not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
