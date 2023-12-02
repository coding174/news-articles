from django.http import HttpResponse, HttpRequest, JsonResponse
from django.shortcuts import render


def main_spa(request: HttpRequest) -> HttpResponse:
    return render(request, 'api/spa/index.html', {})

#sign-up and login views for the application
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .form import PersonForm

from django.shortcuts import get_object_or_404
from .models import Category, NewsArticle

def sign_up(request):
    if request.method == 'POST':
        form = PersonForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile')
    else:
        form = PersonForm()
    return render(request, 'api/spa/sign_up.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('profile')
    else:
        form = AuthenticationForm()
    return render(request, 'api/spa/login.html', {'form': form})

# note: @login_required is a decorator that checks if the user is logged in.

@login_required
def profile(request):
    return render(request, 'api/spa/profile.html')

@login_required
def update_profile(request):
    if request.method == 'POST':
        # Update user profile using request.POST and request.FILES
        return JsonResponse({'status': 'Profile updated successfully'})
    return JsonResponse({'status': 'Profile update failed'})

def news(request):
    categories = Category.objects.all()
    articles_by_category = {}
    for category in categories:
        articles = NewsArticle.objects.filter(category=category) # retrieves all NewsArticle objects that belong to a specific category during each iteration through the categories
        articles_by_category[category] = articles # NewsArticle.objects.filter(category=category): retrieves the articles for each category but assigns the queryset of filtered articles to the articles_by_category dictionary twice, which is unnecessary
    
    context = {
        'articles_by_category': articles_by_category,
        'categories': categories
    }
    return render(request, 'news.html', context)

def get_articles(request):
    articles = NewsArticle.objects.all().values()  # Retrieve all articles as dictionary values
    return JsonResponse({'articles': list(articles)})  # Convert QuerySet to a list and return as JSON

def get_categories(request):
    categories = Category.objects.all().values()  # Retrieve all categories as dictionary values
    return JsonResponse({'categories': list(categories)})  # Convert QuerySet to a list and return as JSON