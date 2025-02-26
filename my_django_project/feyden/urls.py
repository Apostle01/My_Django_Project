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
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from products import views  # Import the views from your 'products' app

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls'), name='home'),  # Home app
    path('bag/', include('bag.urls'), name='bag'),  # Bag app
    path('accounts/', include('allauth.urls')),  # Allauth URLs for user accounts
    path('cloth/', include('cloth.urls')),  # Cloth app URLs
    path('products/', include('products.urls'), name='products'),  # Products app
    path('all-products/', views.all_products, name='all_products'),  # Use 'all_products' view from 'products' app
    path('category/', include('category.urls')),  # Category app URLs
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)






