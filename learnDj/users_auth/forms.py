from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


class UserRegisterFrom(UserCreationForm):
    email = forms.EmailField()
    date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),  # Use HTML5 date input
        label='Date of Birth',
        required=True
    )
    GROUP_CHOICES = [
        ('paid', 'Paid'),
        ('trial', 'Trial'),
    ]
    group = forms.ChoiceField(choices=GROUP_CHOICES, widget=forms.RadioSelect)


    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'date_of_birth', 'group', 'password1', 'password2']