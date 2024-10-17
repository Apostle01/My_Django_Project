from django.shortcuts import render


def index(request):
    """View to return the index.html page"""
    return render(request, 'home/index.html')

def home(request):
    return render(request, 'home.html')
