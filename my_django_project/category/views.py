from django.shortcuts import render

def category_view(request, category_name):
    # Logic to fetch and display products in the category
    context = {
        'category_name': category_name,
        # You can add more context data if needed
    }
    return render(request, 'category/category_page.html', context)

