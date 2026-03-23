from rest_framework import serializers
from .models import Order, OrderItem, Customer
import re

class OrderItemCreateSerializer(serializers.Serializer):
    menu_item_id = serializers.IntegerField()
    size = serializers.ChoiceField(choices=['half', 'full'])
    quantity = serializers.IntegerField(min_value=1, max_value=20)

class PlaceOrderSerializer(serializers.Serializer):
    customer_name = serializers.CharField(max_length=100, min_length=2)
    customer_phone = serializers.CharField(max_length=15)
    delivery_address = serializers.CharField(max_length=500, min_length=10)
    payment_method = serializers.ChoiceField(choices=['cod', 'online'])
    items = OrderItemCreateSerializer(many=True, allow_empty=False)
    special_instructions = serializers.CharField(max_length=500, required=False, allow_blank=True)

    def validate_customer_phone(self, value):
        # Validate 10-digit Indian mobile number
        if not re.match(r'^[6-9]\d{9}$', value):
            raise serializers.ValidationError("Please provide a valid 10-digit Indian mobile number.")
        return value

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'item_name', 'size', 'quantity', 'unit_price', 'total_price']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    customer_name = serializers.CharField(source='customer.name', read_only=True)
    customer_phone = serializers.CharField(source='customer.phone', read_only=True)

    class Meta:
        model = Order
        fields = [
            'order_id', 'customer_name', 'customer_phone', 'delivery_address', 
            'status', 'payment_method', 'payment_status', 'subtotal', 'total', 
            'special_instructions', 'created_at', 'items'
        ]

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['name', 'phone', 'address']
