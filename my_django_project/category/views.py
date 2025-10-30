from django.shortcuts import render, get_object_or_404
from products.models import Category, Product

def category_view(request, foo):
    category = get_object_or_404(Category, name__iexact=foo)
    products = Product.objects.filter(category=category)

    return render(request, "category/category_page.html", {
        "category": category,
        "products": products
    })
