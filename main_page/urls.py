from django.urls import path
from main_page import views

urlpatterns = [
    path('', views.index, name='index'),
    path('search/', views.search, name='search'),
    path('kafolat/', views.coverage, name='coverage'),
]
