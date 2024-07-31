# forms.py
from django import forms
from django.core.validators import RegexValidator
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User  # Import the User model

class CustomUserCreationForm(UserCreationForm):
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(validators=[phone_regex], max_length=17,)
    nrc = forms.CharField(max_length=20)  

    class Meta:
        model = User  
        fields = ['username','email', 'phone_number', 'nrc','password1', 'password2',]
