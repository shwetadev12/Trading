from django.db import models
from decimal import Decimal
from django.core.validators import MinValueValidator


class OrderBook(models.Model):
    class OrderTypes(models.TextChoices):
        BUY = "buy"
        SELL = "sell"

    size = models.PositiveIntegerField()
    price = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal("0.01"))]
    )
    order_type = models.CharField(max_length=5, choices=OrderTypes.choices)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)
