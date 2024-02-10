from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ("category", "title", "description", "image", "price")
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control mb-3', 'style': 'background-color: #F0F0F0; font-size: 1.25rem;'}),
            'title': forms.TextInput(attrs={'class': 'form-control mb-3', 'style': 'background-color: #F0F0F0; font-size: 1.25rem;'}),
            'description': forms.Textarea(attrs={'class': 'form-control mb-3', 'rows': 10, 'style': 'background-color: #F0F0F0; font-size: 1.25rem;'}),
            'image': forms.FileInput(attrs={'class': 'form-control-file mb-3', 'style': 'background-color: #F0F0F0; font-size: 1.25rem;'}),
            'price': forms.NumberInput(attrs={'class': 'form-control mb-3', 'style': 'background-color: #F0F0F0; font-size: 1.25rem;'}),
        }


