import uuid
from user.models import User
from django.db import models


class Order(models.Model):
    ORDER_STATUS = (
        ('placed', 'placed'),
        ('fulfilled', 'fulfilled'),
    )
    SETTLEMENT_STATUS = (
        ('pending', 'pending'),
        ('settled', 'settled'),
    )
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT, null=True)
    token_name = models.CharField(max_length=255)
    quantity = models.DecimalField(max_digits=20, decimal_places=10)
    order_status = models.CharField(choices=ORDER_STATUS, null=True, blank=True, max_length=20)
    settlement_status = models.CharField(choices=SETTLEMENT_STATUS, default='pending', max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
