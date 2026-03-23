from rest_framework import serializers
from .models import Category, MenuItem

class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        # We explicitly list fields to exclude backend-only flags like is_active
        fields = [
            'id', 
            'name', 
            'description', 
            'image', 
            'half_price', 
            'full_price', 
            'is_available', 
            'display_order'
        ]

class CategorySerializer(serializers.ModelSerializer):
    # This will return the related items for each category
    items = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'display_order', 'items']

    def get_items(self, obj):
        # Only return active items for this category
        items = obj.items.filter(is_active=True).order_by('display_order', 'name')
        return MenuItemSerializer(items, many=True).data
