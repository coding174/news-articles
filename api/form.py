from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Person

class PersonForm(UserCreationForm):
    #To get the calendar widget to work, we need to add the type="date" attribute to the widget.
    birth_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    class Meta:
        model = Person
        fields = ('username', 'first_name', 'last_name', 'email', 'birth_date', 'profile_image')