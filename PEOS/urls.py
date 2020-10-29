"""PEOS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path, include
from django.conf.urls import url

from buyer_page.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path(r'buyer/<str:username>/', buyer_landing, name="buyer_landing"),
    path(r'buyer_listing/<str:username>/<str:category>', buyer_listing, name="buyer_listing"),
    path(r'item_details/<str:username>/<int:listing_id>', item_details, name="item_details"),
    path(r'checkout/<str:username>', checkout, name="checkout"),
    path(r'payment/<str:username>', payment, name="payment"),
    path(r'login', login),
]

urlpatterns += [
    path(r'buyer', buyer_landing, name="buyer_landing"),
    path(r'buyer_listing/<str:category>', buyer_listing, name="buyer_listing"),
    path(r'item_details/<int:listing_id>', item_details, name="item_details"),
]

urlpatterns += [
    path(r'seller/<str:username>/', seller_landing, name="seller_landing")
]

"""

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^buyer/(?P<username>\w+?)', buyer_landing, name="buyer_landing"),
    url(r'^buyer_listing/(?P<username>\w+?)/(?P<category>\w+?)', buyer_listing, name="buyer_listing"),
    url(r'^login', login)
]

urlpatterns += [
    url(r'^buyer', buyer_landing, name="buyer_landing"),
    url(r'^buyer_listing/(?P<category>\w+?)', buyer_listing, name="buyer_listing"),
    url(r'^login', login)
]
"""
