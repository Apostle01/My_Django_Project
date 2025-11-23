from django.db import models

class BagItem(models.Model):
    product = models.ForeignKey('store.Product', on_delete=models.CASCADE)
