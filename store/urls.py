from django.urls import path
from . import views

urlpatterns = [
    path('search/',views.search,name='search'), 
    path('add-to-cart/<int:product_id>/',views.add_to_cart,name='add_to_cart'),
    path('update-quantity/<str:product_id>/',views.update_quantity,name="update-quantity"),
    path('cart/',views.cart_view,name='cart_view'),
    path('checkout/',views.checkout,name='checkout'),
    path('paymentgateway/',views.payment_gateway,name='payment'),
    path('payment_success/', views.payment_success, name='payment_success'),
    path('payment_error/', views.payment_error, name='payment_error'),
    path('delete-cart-item/<int:product_id>', views.delete_cart_item,name='delete_cart_item'),
    path('<slug:slug>/', views.category_detail, name='category_detail'),
    path('<slug:category_slug>/<slug:slug>/', views.product_detail, name='product_detail'),
]
