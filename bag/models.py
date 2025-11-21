from django.db import models
from products.models import Product  # Assuming you have a Product model

class Bag(models.Model):
    
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set the creation date
    updated_at = models.DateTimeField(auto_now=True)  # Automatically update the date on save

    def __str__(self):
        return f"{self.user.username}'s Bag"

class BagItem(models.Model):
    bag = models.ForeignKey(Bag, related_name='items', on_delete=models.CASCADE)  # Related to the Bag
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # Link to Product model
    quantity = models.PositiveIntegerField(default=1)  # Number of items

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in {self.bag.user.username}'s Bag"
