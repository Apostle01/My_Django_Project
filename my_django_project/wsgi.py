"""
WSGI config for feyden project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from django.db import connection
from django.db.utils import OperationalError
import time

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'my_django_project.settings')

# Test database connection on startup
try:
    connection.ensure_connection()
    print("✅ Database connection successful")
except OperationalError as e:
    print(f"❌ Database connection failed: {e}")
    # Retry logic
    for i in range(5):
        try:
            time.sleep(2)
            connection.ensure_connection()
            print("✅ Database connection successful after retry")
            break
        except OperationalError:
            print(f"Retry {i+1}/5 failed")

application = get_wsgi_application()
