from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('signup/',views.signup,name='signup'),
    path('logout/',auth_views.LogoutView.as_view(),name='logout'),
    path('login/',auth_views.LoginView.as_view(template_name='userprofile/login.html'),name='login'),
    path('myaccount/',views.myaccount,name='myaccount'),
    path('mystore/',views.mystore,name='mystore'),
    path('mystore/mystore_order_detail/<int:pk>',views.mystore_order_detail,name="mystore-order-detail"),
    path('mystore/vendor_products',views.vendor_products,name='vendor-products'),
    path('mystore/earnings', views.earnings,name='earnings'),
    path('mystore/orders', views.orders,name='orders'),
    path('mystore/add_product/', views.add_product,name='add_product'),
    path('update_order_status/<int:order_id>/', views.update_order_status, name='update_order_status'),
    path('mystore/edit_product/<int:pk>/',views.edit_product,name='edit-product'),
    path('mystore/delete_product/<int:pk>/',views.delete_product,name='delete-product'),
    path('vendors/<int:pk>/', views.vendor_detail, name='vendor_detail'),
]
