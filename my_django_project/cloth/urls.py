from django.urls import path
from . import views

urlpatterns = [
    path('', views.cloth_list, name='cloth_list'),  # List of all cloth items
    path('<int:cloth_id>/', views.cloth_detail, name='cloth_detail'),  # Detail of a specific cloth
    path('add/', views.add_cloth, name='add_cloth'),  # Add a new cloth
    path('edit/<int:cloth_id>/', views.edit_cloth, name='edit_cloth'),  # Edit a cloth item
    path('delete/<int:cloth_id>/', views.delete_cloth, name='delete_cloth'),  # Delete a cloth item
]
