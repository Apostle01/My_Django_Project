from django.urls import path
from . import views

urlpatterns = [
    path('profile/', views.profile, name='profile'),
    path('login/', views.custom_login_view, name='login'),
    # path('logout/', views.custom_logout_view, name='logout'),
    # path('register/', views.custom_register_view, name='register'),
]