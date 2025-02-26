from django import forms
from .models import Product, Review

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['category', 'sku', 'name', 'description', 'price', 'rating', 'image_url', 'image']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['product', 'user', 'rating', 'review']
