"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views

app_name = 'api'
urlpatterns = [
    
    path('customer/login/', views.customer_login, name='customer_login'),
    path('customer/create/', views.customer_create, name='customer_create'),
    path('customer/<int:pk>/', views.customer_get, name='customer_get'),
    path('customer/<int:pk>/picture/add/', views.customer_image_add, name='customer_image_add'),

    path('account/<int:pk>/', views.account_get, name='account_get'),
    path('account/<int:pk>/deposit/', views.account_deposit, name='account_deposit'),

    path('remittance/', views.remittance, name='remittance'),

    path('district/list/', views.district_list, name='district_list'),
    
    path('generate_transation_record/', views.generate_transation_record, name='generate_transation_record'),
    path('default_data/', views.default_data, name='default_data'),
]