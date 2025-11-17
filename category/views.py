from django.shortcuts import render, get_object_or_404
from .models import Category
from store.models import Product

def category_view(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category)

    context = {
        'category': category,
        'products': products,
    }
    return render(request, 'category/category.html', context)

def category_list(request):
    categories = Category.objects.all()
    return render(request, "category/category_list.html", {"categories": categories})
