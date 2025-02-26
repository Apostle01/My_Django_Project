# from django.urls import path
# from . import views

# urlpatterns = [
#     path('', views.cloth_list, name='cloth_list'),  # List of all cloth items
#     path('<int:cloth_id>/', views.cloth_detail, name='cloth_detail'),  # Detail of a specific cloth
#     path('add/', views.add_cloth, name='add_cloth'),  # Add a new cloth
#     path('edit/<int:cloth_id>/', views.edit_cloth, name='edit_cloth'),  # Edit a cloth item
#     path('delete/<int:cloth_id>/', views.delete_cloth, name='delete_cloth'),  # Delete a cloth item
#     path('sort/<str:criterion>/', views.product_sort, name='product_sort'), 
#     path('all/', views.all_products, name='all_products'),
#     path('category/<str:category_name>/', views.category_view, name='category'),
#     path('deals/', views.deals_view, name='deals')
# ]

from django.urls import path
from . import views

urlpatterns = [
    path('', views.cloth_list, name='cloth_list'),  # List view for all cloth
    path('<int:cloth_id>/', views.cloth_detail, name='cloth_detail'),  # Cloth detail view
    path('sort/<str:criterion>/', views.product_sort, name='product_sort'),  # Sorting products
    path('category/<str:category_name>/', views.category_view, name='category'),  # Category filter
    path('deals/', views.deals_view, name='deals'),  # Deals section
]

