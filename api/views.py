from django.http import HttpResponse, HttpRequest, JsonResponse
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .form import PersonForm
from django.shortcuts import get_object_or_404
from .models import Category, NewsArticle, Person
import json
from django.views.decorators.csrf import csrf_exempt

def main_spa(request: HttpRequest) -> HttpResponse:
    return render(request, 'api/spa/index.html', {})

def sign_up(request):
    if request.method == 'POST':
        form = PersonForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # This logs in the user after successful signup
            return redirect(f'http://localhost:5173/')
    else:
        form = PersonForm()
    return render(request, 'api/spa/sign_up.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            # Use authenticate to check the user credentials
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                # The user credentials are valid, log in the user
                login(request, user)
                return redirect(f'http://localhost:5173/')
    else:
        form = AuthenticationForm()
    return render(request, 'api/spa/login.html', {'form': form})

def isUserLoggedIn(request):
    return JsonResponse({'message': request.user.is_authenticated})
# note: @login_required is a decorator that checks if the user is logged in.
@login_required
def person_functions(request):
    if request.method == 'GET':
        person = request.user

        person_data = {
            'id': person.id,
            'username': person.username,
            'first_name': person.first_name,
            'last_name': person.last_name,
            'email': person.email,
            'birth_date': person.birth_date,
            'profile_image': person.profile_image.url if person.profile_image else None,
        }

        print(person_data)
        return JsonResponse({'person': person_data})
    
    if request.method == 'POST':
        try:
            print(request.body)
            data = json.loads(request.body)
            user = request.user

            # Update user data based on the received JSON
            user.first_name = data.get('first_name', user.first_name)
            user.last_name = data.get('last_name', user.last_name)
            user.email = data.get('email', user.email)
            user.birth_date = data.get('birth_date', user.birth_date)
            
            if 'profile_image' in data:
                # Handle profile image update separately
                user.profile_image = handle_profile_image(user, data['profile_image'], user.profile_image)

            user.save()

            return JsonResponse({'message': 'User data updated successfully'}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
        
def handle_profile_image(user, new_image_data, existing_image):
    try:
        # Check if a new image is provided
        if new_image_data:
            # Update or save the new image
            user.profile_image.save(new_image_data.name, new_image_data, save=True)
            
            # Delete the existing image (if any)
            if existing_image:
                existing_image.delete()

            return user.profile_image.url
        elif existing_image:
            # No new image provided, return the existing image URL
            return existing_image.url
        else:
            # No new or existing image, return None or an appropriate default URL
            return None
    except Exception as e:
        # Handle any exceptions that may occur during image handling
        raise e
    
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