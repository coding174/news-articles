import datetime, os
from django.db import models
from django.contrib.auth.models import AbstractUser

# To store the profile image in the media folder
def file_path(request, file_name):
    filename_ext = os.path.splitext(file_name)
    now = datetime.datetime.now()
    file_name = "%s%s" % (now.strftime("%Y%m%d%H%M%S"), filename_ext)
    return os.path.join('profile_image', file_name)

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# To store the user's information
class Person(AbstractUser):
    username = models.CharField(unique=True, max_length=255, null=True, blank=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=False)
    birth_date = models.DateField(null=True, blank=True)
    profile_image = models.ImageField(upload_to=file_path, null=True, blank=True)
    favorite_categories = models.ManyToManyField(Category, blank=True)


class NewsArticle(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Comment(models.Model):
    article = models.ForeignKey(NewsArticle, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(Person, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.article.title}"