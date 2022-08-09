from django.core.management.base import BaseCommand
from OrderBook.models import OrderBook


def check_existing_orders(existing_trades):
    """
    For checking already exiting/matching trades for given order_type and price.
    """
    output = []
    for idx, trade in enumerate(existing_trades):
        if trade.id == id:
            continue
        output.append(
            f" Existing/Matching trade order {idx + 1}: ID {trade.id} | {trade.size} | {trade.price} "
        )
    return output


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("operation", type=str)
        parser.add_argument("--order_type", type=str)
        parser.add_argument("--order_id", type=int)
        parser.add_argument("--size", type=int)
        parser.add_argument("--price", type=int)

    def handle(self, *args, **kwargs):
        id = kwargs.get("order_id")
        operation = kwargs.get("operation")
        order_type = kwargs.get("order_type")
        size = kwargs.get("size")
        price = kwargs.get("price")

        if not operation in ["N", "M", "D"]:
            raise ValueError(
                "Invailid operation please choose N(for new order), M(for modify order) and D(for delete order)! "
            )
        if operation == "N" and not order_type in ["B", "S"]:
            raise ValueError(
                "Invailid order please choose B(for buy order) and S(for sell order)"
            )
        if operation != "D" and price <= 0 and size <= 0:
            raise ValueError("Size and Price must be greater than 0")

        order_type = (
            OrderBook.OrderTypes.BUY.value
            if order_type == "B"
            else OrderBook.OrderTypes.SELL.value
        )

        if operation == "N":
            if order_type == OrderBook.OrderTypes.BUY:
                """
                Trade algo for buy order
                """
                all_sell_order = OrderBook.objects.filter(
                    order_type=OrderBook.OrderTypes.SELL.value
                ).order_by("updated_at")
                if all_sell_order.exists():
                    for sell_order in all_sell_order:
                        if sell_order.price <= price:
                            sell_order.size = sell_order.size - size
                            if sell_order.size <= 0:
                                size = -(sell_order.size)
                                sell_order.delete()
                                if size > 0:
                                    size = size
                    if sell_order.size > 0:
                        sell_order.save()

            if order_type == OrderBook.OrderTypes.SELL.value:
                """
                Trade algo for sell order
                """
                all_buy_order = OrderBook.objects.filter(
                    order_type=OrderBook.OrderTypes.BUY
                ).order_by("price", "updated_at")
                if all_buy_order.exists():
                    for buy_order in all_buy_order:
                        if buy_order.price >= price:
                            buy_order.size = buy_order.size - size
                            size = -(buy_order.size)
                            if buy_order.size <= 0:
                                buy_order.delete()
                                if size > 0:
                                    size = size
                    if buy_order.size > 0:
                        buy_order.save()
            if size > 0:
                """
                If still size is greater than 0 then create an order in OrderBook
                """
                new_order = OrderBook.objects.create(
                    size=size,
                    price=price,
                    order_type=order_type,
                )
            else:
                new_order = False

            type = (
                OrderBook.OrderTypes.BUY
                if order_type == OrderBook.OrderTypes.BUY
                else OrderBook.OrderTypes.SELL.value
            )

            existing_trades = OrderBook.objects.filter(order_type=type, price=price)
            if new_order:
                existing_trades = existing_trades.exclude(id=new_order.id)

            output = check_existing_orders(existing_trades)
            print(output) if output else print("OK")
            return

        elif operation == "M":
            """
            For modifing existing trade order.
            """
            order = OrderBook.objects.get(id=id)
            order.price = price
            order.size = size
            order.save()
            try:
                existing_matching_trades = OrderBook.objects.filter(
                    order_type=order.order_type, price=order.price
                ).exclude(id=id)
                output = check_existing_orders(existing_matching_trades)
                print(output) if output else print("OK")
                return
            except:
                print(f"No trade available for the id: {id}")

        elif operation == "D":
            """
            For deleting existing trade order.
            """
            try:
                order = OrderBook.objects.get(id=id)
                order.delete()
                print("Ok")
            except:
                print(f"No trade available for the id: {id}")
