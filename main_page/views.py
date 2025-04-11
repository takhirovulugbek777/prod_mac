from django.contrib import messages
from django.shortcuts import render

from product.models import Product


def coverage(request):
    if request.method == 'POST':
        serial_number = request.POST.get('serial_number', '').strip()
        product = Product.objects.filter(serial_number=serial_number).first()
        if product:
            return render(request, 'main/coverage.html', {'product': product})
        else:
            messages.success(request, 'Mahsulot topilmadi')
    return render(request, 'main/product_search_form.html')


def index(request):
    return render(request, 'main/index.html')


def search(request):
    return render(request, 'main/product_search_form.html')
