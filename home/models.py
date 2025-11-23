# home/models.py

from django.db import models

class Home(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='home_images/', blank=True, null=True)  # Optional image field
    created_at = models.DateTimeField(auto_now_add=True)  # Creation date
    updated_at = models.DateTimeField(auto_now=True)  # Update date

    def __str__(self):
        return self.title
