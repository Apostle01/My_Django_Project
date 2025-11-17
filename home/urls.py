
from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', views.index, name='home'),
    # path('accounts/', include('allauth.urls')),  # User authentication
    # path('cloth/', include('cloth.urls')),  # Routes to the cloth app (for managing cloths like kente)
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
