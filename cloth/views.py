from django.shortcuts import render, get_object_or_404
from category.models import Category
from products.models import Product


def cloth_list(request):
    # Logic to list all cloth
    return render(request, 'cloth/cloth_list.html')

def cloth_detail(request, cloth_id):
    # Logic for detailed cloth view
    cloth = get_object_or_404(Cloth, id=cloth_id)
    return render(request, 'cloth/cloth_detail.html', {'cloth': cloth})

def category_view(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category)
    return render(request, 'cloth/category_page.html', {
        'category': category,
        'products': products,
    })

def product_sort(request, criterion):
    # Sorting logic for products
    sorted_cloths = Cloth.objects.all().order_by(criterion)
    return render(request, 'cloth/cloth_list.html', {'cloths': sorted_cloths})

def deals_view(request):
    # Logic for the deals view
    return render(request, 'cloth/deals.html')
