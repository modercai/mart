from django.contrib import messages
from django.contrib.auth import login
from django.utils.text import slugify
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from . models import UserProfile
from store.forms import ProductForm 
from store.models import Product,Category

# Create your views here.

def vendor_detail(request,pk):
    user = User.objects.get(pk=pk)
    return render(request,'userprofile/vendor_detail.html',{'user':user})

@login_required
def mystore(request):
    products = request.user.products.exclude(status=Product.DELETED)
    return render(request, 'userprofile/mystore.html',{'products':products})

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
            return redirect('mystore')
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
            return redirect('mystore')
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
    return redirect('mystore')
    

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        
        if form.is_valid():
            user = form.save()
            login(request,user)
            #create a user profile
            userprofile = UserProfile.objects.create(user=user)
            
            return redirect('home')
    else:
            form = UserCreationForm()
    return render(request,'userprofile/signup.html',{'form':form})

@login_required
def myaccount(request):
    return render(request,'userprofile/myaccount.html')