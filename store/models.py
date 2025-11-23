from django.db import models
from django.utils.text import slugify
from cloudinary.models import CloudinaryField

class Product(models.Model):
    name = models.CharField(max_length=200, unique=True)
    slug         = models.SlugField(max_length=200, unique=True)
    description  = models.TextField(max_length=200, unique=True)
    price        = models.IntegerField()
    image        = CloudinaryField('image', folder='products')
    stock        = models.IntegerField()
    is_available = models.BooleanField(default=True)
    category     = models.ForeignKey('category.Category', on_delete=models.CASCADE, related_name="store_products")
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date= models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name
