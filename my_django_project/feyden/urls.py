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
from . import views
from bag import views as bag_views
from django.contrib.auth import views as auth_views
from accounts import views as accounts_views  # Profile view is here

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('bag/', bag_views.bag_view, name='bag'),

    path('accounts/', include('allauth.urls')),  # Using allauth for accounts
    path('cloth/', include('cloth.urls')),  # Cloth app URLs
    
    # Profile view from accounts app
    path('profile/', accounts_views.profile, name='user_profile'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),  # Logout view
]

# Static files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)







