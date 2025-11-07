from django.urls import path
from . import views

urlpatterns = [
    path('', views.view_bag, name='view_bag'),

    # Add to bag
    path('add/<str:item_id>/', views.add_to_bag, name='add_to_bag'),

    # Adjust quantity in bag
    path('adjust/<str:item_id>/', views.adjust_bag, name='adjust_bag'),

    # Remove from bag
    path('remove/<str:item_id>/', views.remove_from_bag, name='remove_from_bag'),
]
