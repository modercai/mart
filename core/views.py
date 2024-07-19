from django.shortcuts import render
from store.models import Product

def home(request):
    products  = Product.objects.all()
    return render(request, 'core/landingpage.html',{'products':products})

def all_products(request):
    products  = Product.objects.all()
    return render(request,'core/all_products.html',{'products':products})

def about(request):
    return render(request, 'core/about.html')