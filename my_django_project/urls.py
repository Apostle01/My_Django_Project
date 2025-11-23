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
# from django.shortcuts import render
# from django.contrib import admin
# from django.urls import path, include
# from django.conf import settings
# from django.conf.urls.static import static
# from products import views  # Import the views from your 'products' app
# from home import views as home_views

# def about(request):
#     return render(request, "about.html")

# def contact(request):
#     return render(request, "contact.html")

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
path('admin/', admin.site.urls),
path('', include('home.urls')),
path('products/', include('products.urls')),
path('category/', include('category.urls')),
path('checkout/', include('checkout.urls')),
path('bag/', include('bag.urls')),
path('accounts/', include('allauth.urls')),
]


if settings.DEBUG:
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)





