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
from .views import main_spa, sign_up, login_view, main_spa, person_functions, isUserLoggedIn, logout_view, profile_image_update
from . import views 

urlpatterns = [
    path('', main_spa),
    path('signup/', sign_up, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('api/isUserLoggedIn/', isUserLoggedIn, name='is_user_logged_in'),
    path('api/getPerson/', person_functions, name='get_person'),
    path('api/editPersonData/', person_functions, name='edit_person_data'),
    path('api/imageUpdate/', profile_image_update, name='profile_image_update'),
    path('api/articles/', views.get_articles, name='get_articles'), # Endpoint for fetching articles
    path('api/categories/', views.get_categories, name='get_categories'), # Endpoint for fetching categories
    path('api/articles/<int:article_id>/comments/', views.get_comments, name='get_comments'),
    path('api/articles/<int:article_id>/create_comment/', views.create_comment, name='create_comment'),
    path('api/edit_comment/<int:comment_id>/', views.edit_comment, name='edit_comment'),
    path('api/delete_comment/<int:comment_id>/', views.delete_comment, name='delete_comment'),
]
