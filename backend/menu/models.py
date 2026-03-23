from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=50)
    display_order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['display_order', 'name']

    def __str__(self):
        return self.name

class MenuItem(models.Model):
    category = models.ForeignKey(Category, related_name='items', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    image = models.URLField(blank=True, help_text="Image URL from Cloudinary or similar service")
    
    half_price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True, help_text="Leave blank if item doesn't have a half size")
    full_price = models.DecimalField(max_digits=8, decimal_places=2)
    
    is_available = models.BooleanField(default=True, help_text="Temporarily out of stock if unchecked")
    is_active = models.BooleanField(default=True, help_text="Soft delete flag")
    display_order = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['category__display_order', 'display_order', 'name']

    def __str__(self):
        return self.name
