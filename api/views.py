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
