from django.shortcuts import render
from store.models import Product

def Home(request):
    products  = Product.objects.all()
    return render(request, 'core/homepage.html',{'products':products})

def about(request):
    return render(request, 'core/about.html')