from django.db import models
from products.models import Product  # Assuming you have a Product model

class Bag(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set the creation date
    updated_at = models.DateTimeField(auto_now=True)      # Automatically update the date on save

    def __str__(self):
        return f"Bag #{self.id}"

class BagItem(models.Model):
    bag = models.ForeignKey(Bag, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"
