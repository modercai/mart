from django.db.models import Q
from django.shortcuts import render, get_object_or_404,redirect
from . models import Product,Category,OrderItem,Order
from . cart import Cart
from . forms import OrderForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse,HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import uuid
import json
from django.conf import settings
import jwt
import requests
from . forms import OrderForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.http import HttpResponse,HttpResponseRedirect



# Create your views here.

def search(request):
    query = request.GET.get('query','')
    products = Product.objects.filter(Q(title__icontains=query) | Q(description__icontains=query))
    return render(request,'store/search.html',{'query':query,'products':products,})
    

def category_detail(request, slug):
    categories = get_object_or_404(Category,slug=slug)
    products = categories.products.all()
    return render(request,'store/category_detail.html',{'categories':categories,'products':products})

def product_detail(request,category_slug, slug):
    product = get_object_or_404(Product,slug= slug)
    return render(request, 'store/product_detail.html',{'product':product})

def add_to_cart(request,product_id):
    cart = Cart(request)
    cart.add(product_id)
    return redirect('cart_view')

def cart_view(request):
    cart = Cart(request)
    return render(request, 'store/cart_view.html',{
        'cart': cart
    })

@login_required
def checkout(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            total_price = 0
            for item in cart:
                product = item['product']
                total_price += product.price * int(item['quantity'])
            order = form.save(commit=False)
            order.created_by = request.user
            order.paid_amount = total_price
            order.save()
            for item in cart:
                product = item['product']
                quantity = int(item['quantity'])
                price = product.price * quantity
                
                item = OrderItem.objects.create(order=order,product=product,price=price, quantity=quantity)
            cart.clear()
            # Store the total amount in the session
            request.session['total_amount'] = total_price
            return redirect('paymentgateway')
    else:
        form = OrderForm()
    return render(request, 'store/checkout.html',{
        'form':form,
        'cart':cart
    })
    
def delete_cart_item(request,product_id):
     cart = Cart(request)
     cart.remove(str(product_id))
     return redirect('cart_view')
 
 
def update_quantity(request,product_id):
    action = request.GET.get('action','')
    
    if action:
        quantity = 1
        
        if action == 'decrease':
            quantity = -1
        cart = Cart(request)
        cart.add(product_id,quantity,True)
    return redirect('cart_view')



@csrf_exempt
def payment_gateway(request):
    url = "https://checkout.sparco.io/gateway/api/v1/checkout"
    
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            address = form.cleaned_data['address']
            address = form.cleaned_data['address']
            phone_number = form.cleaned_data['phone_number']
            
            transaction_reference = str(uuid.uuid4())
            payload = {
                "transactionName": 'Money transfer',
                "amount": 10,
                "currency": "ZMW",
                "transactionReference": transaction_reference,
                "customerFirstName": first_name,
                "customerLastName": last_name,
                "customerEmail": 'malatefriday12@gmail.com',
                "customerPhone": '0972194844',
                "customerAddr": address,
                "customerCity": 'lusaka',
                "customerState": 'lusaka',
                "customerCountryCode": "ZM",
                "customerPostalCode": '10100',
                "merchantPublicKey": "45da9b081b5845a9a3aa1ab4b86c5597",
                "webhookUrl": "https://55ee-165-58-128-152.ngrok-free.app/webhook/",
                "autoReturn": True,
                "chargeMe": True
            }
            
            headers = {
                'Content-Type': 'application/json'
            }
            
            response = requests.post(url, headers=headers, json=payload)
            print(response.text)
            
            try:
                payment_response = response.json()
                payment_url = payment_response.get('paymentUrl')
                return redirect(payment_url)
            except json.JSONDecodeError:
                return JsonResponse({"error": "Invalid response from the payment gateway."}, status=500)
    
    else:
        form = OrderForm()
    
    return render(request, 'checkout.html', {'form': form})

def payment_success(request):
    return render(request, 'store/payment_success.html')

def payment_error(request):
    return render(request, 'store/payment_error.html')

    