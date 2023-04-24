from rest_framework import serializers

from .models import Order


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = 'order_name', 'status', 'linked_account'


class OrderUpdateSerializer(OrderSerializer):
    order_name = serializers.CharField(required=False)
