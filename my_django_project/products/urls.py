from django.urls import path
from . import views

urlpatterns = [
    # All products page (main listing)
    path('', views.all_products, name='all_products'),

    # Product detail
    path('<int:product_id>/', views.product_detail, name='product_detail'),
    path('<int:pk>/', views.product_detail, name='product_detail'),
    # Product management
    path('add/', views.add_product, name='add_product'),
    path('edit/<int:product_id>/', views.edit_product, name='edit_product'),
    path('delete/<int:product_id>/', views.delete_product, name='delete_product'),

    # Reviews
    path('add_review/<int:product_id>/', views.add_review, name='add_review'),
]
