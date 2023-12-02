from django.db import models
from django.contrib.auth.models import AbstractUser

class Person(AbstractUser):
    # Set username to None to avoid conflicts
    username = models.CharField(unique=True, max_length=255, null=True, blank=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=False)
    birth_date = models.DateField(null=True, blank=True)
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)

class Category(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class NewsArticle(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.title