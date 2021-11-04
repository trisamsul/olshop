"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path

from app.api import auth, merchants, order

urlpatterns = [
    path('/', admin.site.urls),

    path('api/v1/auth/login', auth.auth_login),
    path('api/v1/auth/logout', auth.auth_logout),

    path('api/v1/merchants', merchants.get_merchants),
    path('api/v1/merchants/<int:merchant_id>', merchants.get_merchants),

    path('api/v1/products', merchants.get_products),
    path('api/v1/products/<int:product_id>', merchants.get_detail_product),

    path('api/v1/order', order.put_order),
    path('api/v1/order/<int:order_id>', order.get_order_info),

    path('api/v1/payment/confirm/<int:order_id>', order.confirm_payment),
]
