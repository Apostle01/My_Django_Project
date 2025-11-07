# products/urls.py

from django.urls import path
# from cart.views import add_to_cart  # Import your add_to_cart view
from . import views

urlpatterns = [
    # All products page (main listing)
    path('', views.all_products, name='all_products'),

    # Product detail
    path('', views.all_products, name='all_products'),
    path('<int:product_id>/', views.product_detail, name='product_detail'),

    # Product management
    path('add/', views.add_product, name='add_product'),
    path('edit/<int:product_id>/', views.edit_product, name='edit_product'),
    path('delete/<int:product_id>/', views.delete_product, name='delete_product'),

    # Reviews
    path('add-review/<int:product_id>/', views.add_review, name='add_review'),
]
