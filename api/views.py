from django.http import HttpResponse, HttpRequest, JsonResponse
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .form import PersonForm, ImageUpdateForm
from .models import Category, NewsArticle, Person, Comment
import json
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import logout

def main_spa(request: HttpRequest) -> HttpResponse:
    return render(request, 'api/spa/index.html', {})

# Saves the user's data to the database during signup and redirects to the home page
def sign_up(request):
    if request.method == 'POST':
        form = PersonForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')
    else:
        form = PersonForm()
    return render(request, 'api/spa/sign_up.html', {'form': form})

# Checks the user info against the database during login and redirects to the home page
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                return redirect('/')
    else:
        form = AuthenticationForm()
    return render(request, 'api/spa/login.html', {'form': form})

# checks if the user is logged in
def isUserLoggedIn(request):
    return (request.user.is_authenticated)

@login_required
# Fetches information about the user and the allows to update information
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
            'favorite_categories': list(person.favorite_categories.values('id', 'name'))
        }
        favorite_category_ids = person.favorite_categories.values_list('id', flat=True)
        favorite_categories = Category.objects.filter(id__in=favorite_category_ids)

        print("User's favorite categories:", favorite_categories)
        print(person_data)
        return JsonResponse({'person': person_data})
    
    if request.method == 'POST':
        try:
            print(request.body)
            data = json.loads(request.body)
            user = request.user

            user.first_name = data.get('first_name', user.first_name)
            user.last_name = data.get('last_name', user.last_name)
            user.email = data.get('email', user.email)
            user.birth_date = data.get('birth_date', user.birth_date)
        
            user.save()

            if 'favorite_categories' in data:
                user.favorite_categories.clear() 
                favorite_categories = data.get('favorite_categories', [])
                for category_id in favorite_categories:
                    category = Category.objects.get(id=category_id)
                    user.favorite_categories.add(category)
            user.save()

            return JsonResponse({'message': 'User data updated successfully'}, status=200)
        except Category.DoesNotExist:
            return JsonResponse({'error': 'One or more selected categories do not exist'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=405)
        
# Updates the user's profile image
@login_required
def profile_image_update(request):
    if request.method == 'POST':
        image_form = ImageUpdateForm(files = request.FILES, instance=request.user)
        if image_form.is_valid():
            image_form.save()
            return JsonResponse({'message': 'User image updated'}, status=200)
        else:
            return JsonResponse({'error': 'User image not updated'})

# Logs the user out of the system
def logout_view(request):
    logout(request)
    return render(request, 'api/spa/index.html')
    
def news(request):
    categories = Category.objects.all()
    articles_by_category = {}
    for category in categories:
        articles = NewsArticle.objects.filter(category=category) 
        articles_by_category[category] = articles
    
    context = {
        'articles_by_category': articles_by_category,
        'categories': categories
    }
    return render(request, 'news.html', context)

def get_articles(request):
    articles = NewsArticle.objects.all().values() 
    return JsonResponse({'articles': list(articles)})  # Convert QuerySet to a list and return as JSON

def get_categories(request):
    categories = Category.objects.all().values()
    return JsonResponse({'categories': list(categories)})

def get_comments(request, article_id):
    if request.method == 'GET':
        try:
            article = NewsArticle.objects.get(pk=article_id)
            comments = Comment.objects.filter(article=article).values()
            return JsonResponse({'comments': list(comments)})
        except NewsArticle.DoesNotExist:
            return JsonResponse({'error': 'Article does not exist'}, status=404)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

@login_required
@require_POST
def create_comment(request, article_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            content = data.get('content')
            print(content)
            if not content:
                return JsonResponse({'error': 'Invalid data. Please provide content for the comment.'}, status=400)

            article = NewsArticle.objects.get(pk=article_id)
            user = request.user

            comment = Comment.objects.create(user=user, article=article, content=content)
            return JsonResponse({'message': 'Comment created successfully', 'comment_id': comment.id})
        except ObjectDoesNotExist as e:
            return JsonResponse({'error': str(e)}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

@login_required
def edit_comment(request, comment_id):
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            content = data.get('content')

            comment = Comment.objects.get(pk=comment_id, user=request.user)

            comment.content = content
            comment.save()

            return JsonResponse({'message': 'Comment updated successfully'})
        except Comment.DoesNotExist:
            return JsonResponse({'error': 'Comment does not exist or you are not authorized to edit this comment'}, status=404)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

@login_required
def delete_comment(request, comment_id):
    if request.method == 'DELETE':
        try:
            comment = Comment.objects.get(pk=comment_id, user=request.user)
            comment.delete()
            return JsonResponse({'message': 'Comment deleted successfully'})
        except Comment.DoesNotExist:
            return JsonResponse({'error': 'Comment does not exist or you are not authorized to delete this comment'}, status=404)
    return JsonResponse({'error': 'Invalid request method'}, status=405)