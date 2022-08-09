from django.contrib import admin
from django.contrib.auth.models import Group
from OrderBook.models import OrderBook

admin.site.unregister(Group)


@admin.register(OrderBook)
class OrderBookAdmin(admin.ModelAdmin):
    list_display = ["id", "size", "price", "order_type", "updated_at", "created_at"]
    list_filter = ["order_type"]
    ordering = ["price", "updated_at"]
    search_fields = ["size", "price"]
    readonly_fields = ["created_at"]
