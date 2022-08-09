from django.contrib import admin
from django.urls import path
from OrderBook.views import list_orders


urlpatterns = [path("admin/", admin.site.urls), path("", list_orders)]
