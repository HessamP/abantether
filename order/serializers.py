from rest_framework import serializers
from .models import Order


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            'id',
            'user',
            'token_name',
            'quantity',
            'order_status',
            'settlement_status',
            'created_at',
            'last_update'
        ]
