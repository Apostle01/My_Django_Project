"""
URL configuration for my_django_project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.shortcuts import render
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from products import views  # Import the views from your 'products' app
from home import views as home_views

def about(request):
    return render(request, "about.html")

def contact(request):
    return render(request, "contact.html")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')), 
    path('checkout/', include('checkout.urls')),    path('bag/', include('bag.urls'), name='bag'),  # Bag app
    path('accounts/', include('allauth.urls')),  # Allauth URLs for user accounts
    path('products/', include('products.urls')),   # Products app
    path('category/', include('category.urls')),  # Category app URLs
    # path('', views.index, name='home'),  # Make sure you have a home view
    # path('products/', views.all_products, name='all_products'),  # Shop view
    path('about/', about, name='about'),  # About page
    path('contact/', contact, name='contact'),  # Contact page    path('checkout/', include('checkout.urls')),

] 
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)






