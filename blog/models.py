from django.db import models

# Create your models here.

class MovieCategory(models.Model):
    title = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updates_at = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ['created_at']

class MoviePost(models.Model):

    title = models.CharField(max_length=200)
    rating = models.CharField(max_length=10)
    release_year = models.CharField(max_length=10)
    # owner = models.ForeignKey('auth.User',related_name='posts',on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updates_at = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ['created_at']
