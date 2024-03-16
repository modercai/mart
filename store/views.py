from django.db.models import Q
from django.shortcuts import render, get_object_or_404,redirect
from . models import Product,Category,OrderItem,Order
from . cart import Cart
from . forms import OrderForm
from django.contrib.auth.decorators import login_required


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
            return redirect('myaccount')
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