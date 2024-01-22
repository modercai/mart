from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('signup/',views.signup,name='signup'),
    path('logout/',auth_views.LogoutView.as_view(),name='logout'),
    path('login/',auth_views.LoginView.as_view(template_name='userprofile/login.html'),name='login'),
    path('myaccount/',views.myaccount,name='myaccount'),
    path('mystore/',views.mystore,name='mystore'),
    path('mystore/add_product/', views.add_product,name='add_product'),
    path('mystore/edit_product/<int:pk>/',views.edit_product,name='edit-product'),
    path('mystore/delete_product/<int:pk>/',views.delete_product,name='delete-product'),
    path('vendors/<int:pk>/', views.vendor_detail, name='vendor_detail'),
]
