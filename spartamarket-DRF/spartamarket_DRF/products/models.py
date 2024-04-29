# products/models.py

from django.db import models

class Product(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='products/')

    # Add any other fields as needed
