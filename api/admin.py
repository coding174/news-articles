from django.contrib import admin

from .models import Person, NewsArticle, Category, Comment

admin.site.register(Person)

admin.site.register(NewsArticle)
admin.site.register(Category)

class CommentAdmin(admin.ModelAdmin):
    list_display = ('content', 'user')

admin.site.register(Comment, CommentAdmin)