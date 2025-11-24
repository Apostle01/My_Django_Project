from django.shortcuts import render


def index(request):
    """View to return the index.html page"""
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

