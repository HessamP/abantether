from django.contrib import admin
from .models import User,Balance


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'email',
        'first_name',
        'last_name',
        'is_staff',
        'is_admin',
        'is_superuser',
        'is_active',
        'created_date'
    ]

@admin.register(Balance)
class BalanceAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'amount',
        'blocked_amount',
        'last_update',
    ]
    fields = [
        'user',
        'blocked_amount',
        'amount'
    ]
