from django.contrib import admin

from .models import Person, NewsArticle, Category

admin.site.register(Person)

admin.site.register(NewsArticle)
admin.site.register(Category)
