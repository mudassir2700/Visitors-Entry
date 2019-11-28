
app_name='assignment'
from django.contrib import admin
from django.urls import path,include
from .import views

urlpatterns = [
       path('',views.homepage,name='index'),
       path('signup/', views.register,name='signup'),
       path('login/', views.login_view,name='login'),
       path('booking/', views.booking_view,name='booking'),
       path('checkout/', views.checkout_view,name='checkout'),
]
