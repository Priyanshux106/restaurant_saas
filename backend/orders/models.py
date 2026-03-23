from django.db import models

class Customer(models.Model):
    phone = models.CharField(max_length=15, unique=True, db_index=True)
    name = models.CharField(max_length=100)
    address = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.phone})"

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('preparing', 'Preparing'),
        ('ready', 'Ready'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    PAYMENT_CHOICES = [
        ('cod', 'Cash on Delivery'),
        ('online', 'Online Payment'),
    ]
    
    order_id = models.CharField(max_length=20, unique=True, db_index=True)
    customer = models.ForeignKey(Customer, related_name='orders', on_delete=models.CASCADE)
    delivery_address = models.TextField()
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_method = models.CharField(max_length=10, choices=PAYMENT_CHOICES)
    payment_status = models.CharField(max_length=20, default='pending')
    payment_id = models.CharField(max_length=100, blank=True, help_text="Razorpay payment ID")
    
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    special_instructions = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.order_id} - {self.customer.name} - {self.status}"

class OrderItem(models.Model):
    SIZE_CHOICES = [('half', 'Half'), ('full', 'Full')]
    
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    # Using PROTECT because we don't want to delete an order item if a menu item is deleted.
    menu_item = models.ForeignKey('menu.MenuItem', on_delete=models.PROTECT)
    
    # We snapshot these fields because price/name might change in the menu
    # but shouldn't change for past orders
    item_name = models.CharField(max_length=100)
    size = models.CharField(max_length=4, choices=SIZE_CHOICES)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=8, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity}x {self.item_name} ({self.size})"
