from django import forms
from .models import Product, Order

class BaseStyledForm:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition duration-300',
            })

class OrderForm(BaseStyledForm, forms.ModelForm):
    class Meta:
        model = Order
        fields = ("first_name", "last_name", "address", "town", "phone_number")
        
        labels = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'address': 'Delivery Address',
            'town': 'City/Town',
            'phone_number': 'Contact Number'
        }
        
        error_messages = {
            'phone_number': {
                'invalid': 'Please enter a valid phone number.',
            },
        }

    def clean_phone_number(self):
        phone = self.cleaned_data['phone_number']
        # Basic phone number validation
        if not phone.isdigit():
            raise forms.ValidationError("Phone number must contain only digits.")
        return phone

class ProductForm(BaseStyledForm, forms.ModelForm):
    class Meta:
        model = Product
        fields = ("category", "title", "description", "image", "price")
        
        labels = {
            'category': 'Product Category',
            'title': 'Product Name',
            'description': 'Product Description',
            'image': 'Product Image',
            'price': 'Price (USD)'
        }
        
        help_texts = {
            'description': 'Provide a detailed description of the product.',
            'image': 'Upload a clear image of the product (max 5MB)',
            'price': 'Enter the price in USD'
        }
        
        widgets = {
            'category': forms.Select(attrs={'class': 'select-styling'}),
            'description': forms.Textarea(attrs={'rows': 5}),
            'image': forms.ClearableFileInput(attrs={'class': 'file-input-styling'}),
        }

    def clean_price(self):
        price = self.cleaned_data['price']
        if price <= 0:
            raise forms.ValidationError("Price must be a positive number.")
        return price

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            # Optional: Add image size validation
            if image.size > 5 * 1024 * 1024:  # 5MB limit
                raise forms.ValidationError("Image file too large. Max 5MB.")
        return image