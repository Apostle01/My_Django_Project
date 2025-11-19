from django.apps import AppConfig
from django.db import connection
import logging

logger = logging.getLogger(__name__)

class HomeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'home'

    def ready(self):
        self.test_db_connection()

    def test_db_connection(self):
        try:
            connection.ensure_connection()
            logger.info("Database is reachable.")
        except Exception as e:
            logger.error(f"Unable to connect to database: {e}")
