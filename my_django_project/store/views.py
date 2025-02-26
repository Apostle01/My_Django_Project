from django.shortcuts import render

def store_view(request):
    return render(request, 'store/store.html')  # Ensure 'store.html' exists in the 'store/templates/store' directory
