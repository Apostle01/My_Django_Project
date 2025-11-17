from django.shortcuts import get_object_or_404, render
from .models import Product
from category.models import Category

def category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category)
    return render(request, "store/category.html", {
        "category": category,
        "products": products,
    })


# from django.shortcuts import render

# def store(request):
#     return render(request, "store.html")  # Ensure 'store.html' exists in the 'store/templates/store' directory
