from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class Person(AbstractUser):
    # Set username to None to avoid conflicts
    username = models.CharField(unique=True, max_length=255, null=True, blank=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=False)
    birth_date = models.DateField(null=True, blank=True)
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)