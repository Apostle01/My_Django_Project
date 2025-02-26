# category/urls.py
from django.urls import path
from . import views  # Import views from the current package

urlpatterns = [
    path('<slug:category_name>/', views.category_view, name='category'),  # Now 'views' is defined
]
