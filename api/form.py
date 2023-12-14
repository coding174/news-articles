from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Person

# Used when user signs up to the app
class PersonForm(UserCreationForm):
    birth_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    class Meta:
        model = Person
        fields = ('username', 'first_name', 'last_name', 'email', 'birth_date', 'profile_image')


# Used when user updates their profile image
class ImageUpdateForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ['profile_image']