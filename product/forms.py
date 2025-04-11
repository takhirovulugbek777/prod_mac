from django import forms
from .models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'name',
            'warranty_period',
            'sold_date',
            'serial_number',
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control',
                                           'placeholder': 'Enter product name'}),

            'warranty_period': forms.NumberInput(
                attrs={'class': 'form-control',
                       'placeholder': 'Enter warranty period in months'}),
            'sold_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'serial_number': forms.TextInput(attrs={'class': 'form-control',
                                                    'placeholder': 'Enter serial number'}),

        }
        labels = {
            'name': 'Product Name',
            'warranty_period': 'Warranty Period (Months)',
            'sold_date': 'Date Sold',
            'serial_number': 'Serial Number',

        }
        help_texts = {
            'name': 'Name of the product.',
            'warranty_period': 'Duration of warranty in months.',
            'sold_date': 'Date when the product was sold.',
            'serial_number': 'A unique identifier for the product.',

        }


class ClientForm(forms.Form):
    class Meta:
        fields = '__all__'
