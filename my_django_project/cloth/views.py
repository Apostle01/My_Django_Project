from django.shortcuts import render, get_object_or_404
from .models import Cloth, Category

def cloth_list(request):
    # Logic to list all cloth
    return render(request, 'cloth/cloth_list.html')

def cloth_detail(request, cloth_id):
    # Logic for detailed cloth view
    cloth = get_object_or_404(Cloth, id=cloth_id)
    return render(request, 'cloth/cloth_detail.html', {'cloth': cloth})

def category_view(request, category_name):
    # Logic for category view
    category = get_object_or_404(Category, name=category_name)
    cloths = Cloth.objects.filter(category=category)
    return render(request, 'cloth/category.html', {'category': category, 'cloths': cloths})

def product_sort(request, criterion):
    # Sorting logic for products
    sorted_cloths = Cloth.objects.all().order_by(criterion)
    return render(request, 'cloth/cloth_list.html', {'cloths': sorted_cloths})

def deals_view(request):
    # Logic for the deals view
    return render(request, 'cloth/deals.html')
