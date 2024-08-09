from django.contrib import messages
from django.contrib.auth import login
from django.utils.text import slugify
from django.shortcuts import redirect, render,get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.core.paginator import Paginator
from store import models
from django.urls import reverse
from . models import UserProfile
from store.forms import ProductForm 
from store.models import Product,OrderItem,Order
from . forms import CustomUserCreationForm
from .tables import OrderTable
from django.db.models import Sum

# Create your views here.

def vendor_detail(request,pk):
    user = User.objects.get(pk=pk)
    return render(request,'userprofile/vendor_detail.html',{'user':user})

@login_required
def mystore(request):
    products = request.user.products.exclude(status=Product.DELETED)
    order_items = OrderItem.objects.filter(product__user=request.user)
    return render(request, 'userprofile/dashboard/dashboard.html',{'products':products,'order_items':order_items})

@login_required
def mystore_order_detail(request, pk):
    order = get_object_or_404(Order,pk=pk)
    return render(request, 'userprofile/mystore_order_detail.html',{'order':order,})

def orders_view(request):
    order_items = OrderItem.objects.all()
    table = OrderTable(order_items)
    print(table) 
    return render(request, 'userprofile/dashboard/dashboard.html', {'table': table})

#allow the vendor to change the order status of the item
@login_required
def update_order_status(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == "POST":
        status = request.POST.get("status")
        order.status = status
        order.save()
        return redirect(reverse('orders'))
    
 #remove this if it doesnt work!!!   
@login_required
def total_price_all_order_items(request):
    total_price = OrderItem.objects.aggregate(total_price=models.Sum('price'))['total_price']
    return render(request, 'userprofile/dashboard/earnings.html', {'total_order_price': total_price})

@login_required
def total_price_delivered_orders(request):
    total_price = Order.objects.filter(user=request.user, status='delivered').aggregate(total_price=models.Sum('total_price'))['total_price']
    return render(request, 'userprofile/dashboard/earnings.html', {'total_earned_price': total_price})
    

@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            title = request.POST.get('title')
            product = form.save(commit=False)
            product.user = request.user
            product.slug = slugify(title)
            product.save()
            messages.success(request, "Product added successfully.") 
            return redirect('vendor-products')
    else:
        form = ProductForm()
    return render(request, 'userprofile/add_product.html',{
        'title': 'Add product',
        'form':form})


@login_required
def edit_product(request,pk):
    product = Product.objects.filter(user=request.user).get(pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, "Product details updated successfully.")
            return redirect('vendor-products')
    else:
        form = ProductForm(instance=product)
    return render(request, 'userprofile/add_product.html',{
        'title':'Edit product',
        'product':product,
        'form':form})
    
@login_required
def delete_product(request,pk):
    product = Product.objects.filter(user=request.user).get(pk=pk)
    product.status = Product.DELETED
    product.save()
    messages.success(request, "Product was deleted successfully.")
    return redirect('vendor-products')
    

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # Handle additional fields
            user.email = form.cleaned_data['email']
            user.nrc = form.cleaned_data['nrc']
            user.phone_number = form.cleaned_data['phone_number']
            # Save the user
            user.save()
            UserProfile.objects.create(user=user)
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'userprofile/signup.html', {'form': form})

@login_required
def myaccount(request):
    return render(request,'userprofile/myaccount.html')


@login_required
def vendor_products(request):
    products = request.user.products.exclude(status=Product.DELETED)
    return render(request, 'userprofile/dashboard/product.html',{'products':products})

@login_required
def earnings(request):
    return render(request, 'userprofile/dashboard/earnings.html')

@login_required
def orders(request):
    order_items = OrderItem.objects.filter(product__user=request.user)
    products = request.user.products.exclude(status=Product.DELETED)
    return render(request, 'userprofile/dashboard/orders.html',{'order_items':order_items,})

# data to be displayed on the database
def dashboard(request):
    status_counts = Product.objects.values('status').annotate(count=models.Count('id'))
    labels = [status['status'] for status in status_counts]
    data = [status['count'] for status in status_counts]
    return render(request, 'userprofile/dashboard/dashboard.html',{'labels': labels, 'data': data})

