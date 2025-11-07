from django.shortcuts import render

def store(request):
    return render(request, "store.html")  # Ensure 'store.html' exists in the 'store/templates/store' directory
