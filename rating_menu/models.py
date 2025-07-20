from django.db import models

# Create your models here.
class MediaItem(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='media_items', default=None, null=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    rating = models.IntegerField(blank=True, null=True)  # Assuming rating is an integer
    poster_url = models.URLField(default="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS0OCD8vwRqyldCWESsUQ9_r2YQzHMPHXi1MQ&s")  # Default poster URL
    tmdb_id = models.IntegerField(default=0)  # Assuming tmdb_id is an integer
    created_at = models.DateTimeField(auto_now_add=True)
    genre = models.CharField(max_length=100, blank=True, null=True)
    year = models.DateField(blank=True, null=True)
    type = models.SlugField()
    

    def __str__(self):
        return f"{self.title} {self.description} ({self.rating}/10) {self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else 'N/A'}" 