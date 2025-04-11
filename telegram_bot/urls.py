from django.urls import path

from telegram_bot import views
from telegram_bot.views import ProductDetailView, TelegramUserCreateApiView, CreditCalculationAPIView

urlpatterns = [
    path('products/<str:serial_number>/', ProductDetailView.as_view(), name='product-detail'),
]

urlpatterns += [
    path('usercreate/', TelegramUserCreateApiView.as_view()),
    path('category/<int:cat_pk>/', CreditCalculationAPIView.as_view(), name='category-detail'), ]
