from rest_framework import serializers
from .models import StoreSettings

class StoreStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoreSettings
        fields = ['is_open', 'min_order_value', 'store_name', 'estimated_delivery_time']
