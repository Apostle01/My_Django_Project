# from django.shortcuts import render
# from store.models import Product
# from django.http import HttpResponse

# # Home view
# def home(request):
#     product = Product.object.all().filter(is_available=True)

#     context = {
#         'products': products,
#     }
#     return render(request, 'home.html', context)  # Ensure home.html exists in your templates directory

# def profile(request):
#     return render(request, 'profile.html')  # Adjust the template name as necessary

# def bag_view(request):
#     return render(request, 'bag/bag.html')

from django.shortcuts import render

def checkout(request):
    """
    Simple placeholder checkout page.
    """
    return render(request, 'checkout/checkout.html')

