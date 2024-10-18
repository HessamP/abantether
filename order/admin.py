from django.contrib import admin
from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'user',
        'token_name',
        'quantity',
        'order_status',
        'settlement_status',
        'created_at',
        'last_update'
    ]

    fields = [
        'user',
        'token_name',
        'quantity',
        'order_status',
        'settlement_status',
    ]
