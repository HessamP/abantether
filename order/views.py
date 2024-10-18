from django.db import transaction
from django.db.models import Q
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from user.models import Balance
from .models import Order
from .serializers import OrderSerializer
from .utils import buy_from_exchange
from decimal import Decimal


class OrderView(APIView):
    PRICE = Decimal(4.0)

    def post(self, request):
        user = request.user
        serializer = OrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token_name = serializer.validated_data.get('token_name')
        quantity = Decimal(serializer.validated_data.get('quantity'))

        user_balance_qs = self.get_user_balance(user)
        if not user_balance_qs:
            return Response({"detail": "Error during fetching user balance"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        request_amount = quantity * self.PRICE

        if not self.has_sufficient_balance(user_balance_qs, request_amount):
            return Response({"detail": "Insufficient balance"}, status=status.HTTP_400_BAD_REQUEST)

        self.block_user_funds(user_balance_qs, request_amount)

        if request_amount >= 10.0:
            return self.process_gte_10_dollars_order(user, token_name, quantity, user_balance_qs, request_amount)

        elif request_amount <= 0:
            return Response({"detail": "Invalid quantity"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return self.process_small_order(user, token_name, quantity, user_balance_qs, request_amount)

    def get_user_balance(self, user):
        try:
            return Balance.objects.get(user=user)
        except Exception as e:
            return None

    def has_sufficient_balance(self, balance, amount):
        return balance.available_balance() >= amount

    def block_user_funds(self, balance, amount):
        with transaction.atomic():
            balance.blocked_amount += amount
            balance.order_status = 'placed'
            balance.save()

    def process_gte_10_dollars_order(self, user, token_name, quantity, user_balance, amount):
        with transaction.atomic():
            buy_from_exchange(token_name, quantity)
            self.create_order(user, token_name, quantity, 'settled', 'fulfilled')
            self.update_user_balance_after_settlement(user_balance, amount)

        return Response({"detail": "Order placed and settled successfully"}, status=status.HTTP_200_OK)

    def create_order(self, user, token_name, quantity, settlement_status, order_status):
        return Order.objects.create(
            user=user, token_name=token_name, quantity=quantity,
            settlement_status=settlement_status, order_status=order_status
        )

    def update_user_balance_after_settlement(self, user_balance, amount):
        user_balance.blocked_amount -= amount
        user_balance.amount -= amount
        user_balance.save()

    def process_small_order(self, user, token_name, quantity, user_balance, amount):
        pending_orders = self.get_pending_orders()
        total_pending_amount = 0

        for order in pending_orders:
            total_pending_amount += order.quantity * self.PRICE

        if amount + total_pending_amount >= 10.0:
            return self.settle_orders(user, token_name, quantity, user_balance, amount, pending_orders)

        with transaction.atomic():
            self.create_order(user, token_name, quantity, 'pending', 'placed')

        return Response({"detail": "Order placed and pending settlement"}, status=status.HTTP_200_OK)

    def get_pending_orders(self):
        return Order.objects.filter(~Q(settlement_status='settled') & Q(quantity__lte=2))

    def settle_orders(self, user, token_name, quantity, user_balance, amount, pending_orders):
        total_quantity = quantity
        total_amount = amount

        for order in pending_orders:
            order_quantity = order.quantity
            order_amount = order_quantity * self.PRICE

            total_quantity += order_quantity
            total_amount += order_amount
        with transaction.atomic():
            buy_from_exchange(token_name, total_quantity)
            self.create_order(user, token_name, quantity, 'settled', 'fulfilled')
            self.update_user_balance_after_settlement(user_balance, amount)

            for order in pending_orders:
                self.settle_existing_order(order)

        return Response({"detail": "Order placed and settled, pending orders settled as well successfully"},
                        status=status.HTTP_200_OK)

    def settle_existing_order(self, order):
        order.order_status = 'fulfilled'
        order.settlement_status = 'settled'
        order.save()

        user_balance = Balance.objects.get(user=order.user)
        order_amount = order.quantity * self.PRICE
        user_balance.blocked_amount -= order_amount
        user_balance.amount -= order_amount
        user_balance.save()
