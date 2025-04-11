from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError, transaction
from django.db.models import Q, Count
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.timezone import now, make_aware
from django.views import View
from django.views.generic import (
    TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.core.paginator import Paginator

import openpyxl
from openpyxl.styles import Font
import random
import io
from datetime import datetime, timedelta

from .models import Product, Client
from .forms import ProductForm


# Home and Authentication Views
class HomeView(TemplateView):
    template_name = 'v2/home.html'


class LoginView(View):
    template_name = 'v2/login.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'Logged In!')
            return redirect('home')
        else:
            messages.error(request, 'Please try again.....')
            return redirect('login')


class LogoutView(View):
    def get(self, request):
        logout(request)
        messages.success(request, 'Success Logout!')
        return redirect('home')


# Product Views
class ProductListView(ListView):
    model = Product
    template_name = 'v2/product_table.html'
    context_object_name = 'page_obj'
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get('q', '')
        queryset = Product.objects.filter(
            Q(name__icontains=query) |
            Q(serial_number__icontains=query) |
            Q(client__phone__icontains=query) |
            Q(client__name__icontains=query)
        ).select_related('client')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'v2/product_detail.html'
    context_object_name = 'product'


@method_decorator(login_required, name='dispatch')
class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'v2/product_form.html'
    success_url = reverse_lazy('product_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create New Product'
        return context

    @transaction.atomic
    def form_valid(self, form):
        client_name = self.request.POST.get('client_name')
        client_phone = self.request.POST.get('client_phone')

        if not client_name or not client_phone:
            form.add_error(None, 'Client name and phone are required')
            return self.form_invalid(form)

        try:
            client, created = Client.objects.get_or_create(
                phone=client_phone,
                defaults={'name': client_name}
            )

            if not created and client.name != client_name:
                client.name = client_name
                client.save()

            product = form.save(commit=False)
            product.client = client
            product.save()

            messages.success(self.request, 'Product created successfully!')
            return super().form_valid(form)

        except IntegrityError:
            form.add_error(None, 'An error occurred. '
                                 'The phone number might be associated with another client.')
            return self.form_invalid(form)


@method_decorator(login_required, name='dispatch')
class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'v2/product_form.html'
    success_url = reverse_lazy('product_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edit Product'
        context['client_name'] = self.object.client.name if self.object.client else ''
        context['client_phone'] = self.object.client.phone if self.object.client else ''
        return context

    @transaction.atomic
    def form_valid(self, form):
        client_name = self.request.POST.get('client_name')
        client_phone = self.request.POST.get('client_phone')

        if not client_name or not client_phone:
            form.add_error(None, 'Client name and phone are required')
            return self.form_invalid(form)

        try:
            client, created = Client.objects.get_or_create(
                phone=client_phone,
                defaults={'name': client_name}
            )

            if not created and client.name != client_name:
                client.name = client_name
                client.save()

            product = form.save(commit=False)
            product.client = client
            product.save()

            messages.success(self.request, 'Product updated successfully!')
            return super().form_valid(form)

        except IntegrityError:
            form.add_error(None, 'An error occurred. '
                                 'The phone number might be associated with another client.')
            return self.form_invalid(form)


@method_decorator(login_required, name='dispatch')
class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'v2/product_confirm_delete.html'
    success_url = reverse_lazy('product_list')

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        messages.success(request, 'Product deleted successfully!')
        return response


# Client Views
class ClientListView(ListView):
    model = Client
    template_name = 'v2/client_table.html'
    context_object_name = 'page_obj'
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get('q', '')
        return Client.objects.annotate(
            product_count=Count('products')
        ).filter(
            Q(name__icontains=query) | Q(phone__icontains=query)
        ).order_by('name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        return context


class ClientDetailView(DetailView):
    model = Client
    template_name = 'v2/client_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products = self.object.products.all()

        paginator = Paginator(products, 10)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context['page_obj'] = page_obj
        context['title'] = f"Client Details: {self.object.name}"
        return context


@method_decorator(login_required, name='dispatch')
class ClientUpdateView(UpdateView):
    model = Client
    template_name = 'v2/client_update.html'
    fields = ['name', 'phone']
    success_url = reverse_lazy('client_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Client updated successfully!')
        return response


# Excel Export Views
class ExcelPageView(TemplateView):
    template_name = 'v2/exel/exel_download.html'


class ExportProductsView(View):
    def generate_captcha(self, request):
        num1 = random.randint(1, 10)
        num2 = random.randint(1, 10)
        request.session['captcha_result'] = num1 + num2
        return {'num1': num1, 'num2': num2}

    def validate_captcha(self, request):
        try:
            user_result = int(request.POST.get('captcha_result', 0))
            correct_result = request.session.get('captcha_result')
            return user_result == correct_result
        except (ValueError, TypeError):
            return False

    def check_request_limit(self, request):
        current_time = now()
        request_times = request.session.get('request_times', [])

        # Filter out old requests
        try:
            request_times = [
                make_aware(datetime.strptime(time, "%Y-%m-%d %H:%M:%S"))
                for time in request_times if
                make_aware(datetime.strptime(time, "%Y-%m-%d %H:%M:%S"))
                > current_time - timedelta(minutes=1)
            ]
        except (ValueError, TypeError):
            request_times = []

        # Check if limit exceeded
        if len(request_times) >= 3:
            block_until = current_time + timedelta(hours=1)
            request.session['blocked_until'] = block_until.strftime("%Y-%m-%d %H:%M:%S")
            return block_until

        # Update request times
        request_times.append(current_time.strftime("%Y-%m-%d %H:%M:%S"))
        request.session['request_times'] = request_times
        return None

    def generate_excel(self):
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        sheet.title = "Products"

        # Add headers
        headers = [
            "ID", "Product Name", "Serial Number", "Client Name", "Sold Date",
            "Warranty Period (Months)", "Is Warranty Active", "Created At"
        ]
        sheet.append(headers)

        # Style headers
        for cell in sheet[1]:
            cell.font = Font(bold=True)

        # Set column widths
        column_widths = [10, 20, 20, 25, 15, 25, 20, 20]
        for i, width in enumerate(column_widths, start=1):
            sheet.column_dimensions[openpyxl.utils.get_column_letter(i)].width = width

        # Add product data
        products = Product.objects.select_related('client').all()
        for product in products:
            row = [
                product.id,
                product.name,
                product.serial_number,
                product.client.name if product.client else "No Client",
                product.sold_date,
                product.warranty_period,
                "Active" if product.is_warranty_active else "Expired",
                product.created_at.replace(tzinfo=None),
            ]
            sheet.append(row)

        # Save to BytesIO
        excel_file = io.BytesIO()
        workbook.save(excel_file)
        excel_file.seek(0)
        return excel_file

    def get(self, request):
        # Check if user is blocked
        blocked_until = request.session.get('blocked_until')
        if blocked_until:
            try:
                blocked_until = make_aware(datetime.strptime(blocked_until, "%Y-%m-%d %H:%M:%S"))
                if blocked_until > now():
                    messages.error(request, 'You are temporarily blocked! Please try again later.')
                    return redirect('home')
            except (ValueError, TypeError):
                # If there's an error parsing the date, clear the block
                request.session.pop('blocked_until', None)

        # Show captcha form
        captcha = self.generate_captcha(request)
        return render(request, 'v2/exel/export_captcha.html', captcha)

    def post(self, request):
        # Validate captcha
        if not self.validate_captcha(request):
            captcha = self.generate_captcha(request)
            return render(request, 'v2/exel/export_captcha.html',
                          {**captcha, 'error': 'Incorrect CAPTCHA! Try again.'})

        # Check request limit
        block_until = self.check_request_limit(request)
        if block_until:
            messages.error(request, f'You are temporarily blocked until {block_until}.')
            return redirect('home')

        # Render download page with JavaScript
        messages.success(request, 'Excel file has been successfully generated and downloaded.')
        return render(request, 'v2/exel/download_and_redirect.html', {
            'file_url': reverse('download_excel'),
            'redirect_url': reverse('home')
        })


class DownloadExcelView(View):
    def get(self, request):
        # Generate Excel file
        excel_generator = ExportProductsView()
        excel_file = excel_generator.generate_excel()

        # Create response
        response = HttpResponse(
            excel_file.getvalue(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename=products.xlsx'
        return response
