from django.shortcuts import render
from .models import OrderBook


def list_orders(request):
    buy_type = OrderBook.objects.filter(
        order_type=OrderBook.OrderTypes.BUY.value
    ).order_by("-price", "updated_at")
    sell_type = OrderBook.objects.filter(
        order_type=OrderBook.OrderTypes.SELL.value
    ).order_by("price", "updated_at")
    context = {"buy": buy_type, "sell": sell_type}
    return render(request, "order_list.html", context)
