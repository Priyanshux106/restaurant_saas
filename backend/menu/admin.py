from django.contrib import admin
from .models import Category, MenuItem

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'display_order', 'is_active')
    list_editable = ('display_order', 'is_active')
    search_fields = ('name',)

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'half_price', 'full_price', 'is_available', 'is_active', 'display_order')
    list_filter = ('category', 'is_available', 'is_active')
    list_editable = ('is_available', 'is_active', 'display_order')
    search_fields = ('name', 'description')
