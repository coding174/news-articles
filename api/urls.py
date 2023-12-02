"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.http import HttpResponse
from .views import main_spa, sign_up, login_view, profile, update_profile, main_spa
from . import views 

urlpatterns = [
    path('', main_spa),
    path('signup/', sign_up, name='signup'),
    path('login/', login_view, name='login'),
    path('profile/', profile, name='profile'),
    path('profile/update/', update_profile, name='update_profile'),
    # Endpoint for fetching articles
    path('api/articles/', views.get_articles, name='get_articles'),

    # Endpoint for fetching categories
    path('api/categories/', views.get_categories, name='get_categories'),
]
