from django.db import models

# Create your models here.
class MediaItem(models.Model):
    search_field = models.CharField(max_length=100)