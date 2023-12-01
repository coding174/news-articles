from django.contrib import admin

from .models import Person

class PersonAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email', 'date_joined')

admin.site.register(Person, PersonAdmin)