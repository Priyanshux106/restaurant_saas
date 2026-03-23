from django.db import models

class StoreSettings(models.Model):
    is_open = models.BooleanField(default=True)
    min_order_value = models.DecimalField(max_digits=8, decimal_places=2, default=200)
    store_name = models.CharField(max_length=200, default='Restaurant')
    store_phone = models.CharField(max_length=15, default='')
    owner_whatsapp = models.CharField(max_length=15, default='')   # For notifications
    estimated_delivery_time = models.IntegerField(default=45, help_text="In minutes")  
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Store Settings"

    def __str__(self):
        return f"{self.store_name} Settings"

    def save(self, *args, **kwargs):
        # Ensure there's only one StoreSettings instance
        if not self.pk and StoreSettings.objects.exists():
            return
        return super().save(*args, **kwargs)
