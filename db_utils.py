# db_utils.py
from django.db import connection
from django.db.utils import OperationalError
import time

def test_db_connection(max_retries=5, delay=2):
    for attempt in range(max_retries):
        try:
            connection.ensure_connection()
            return True
        except OperationalError:
            if attempt < max_retries - 1:
                time.sleep(delay)
                continue
            else:
                raise
                