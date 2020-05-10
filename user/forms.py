from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from django.forms import TextInput, EmailInput, Select, FileInput
from home.models import UserProfile


class UserUpdateForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')
        widgets = {
            'username': TextInput(attrs={'class': 'input', 'placeholder': 'username'}),
            'username': EmailInput(attrs={'class': 'input', 'placeholder': 'email'}),
            'username': TextInput(attrs={'class': 'input', 'placeholder': 'first_name'}),
            'username': TextInput(attrs={'class': 'input', 'placeholder': 'last_name'}),
        }


CITY = [
    ('Istanbul', 'Istanbul'),
    ('Izmir', 'Izmir'),
    ('Konya', 'Konya'),
    ('Ankara', 'Ankara'),
]


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('phone', 'address', 'city', 'country', 'image')
        widgets = {
            'phone': TextInput(attrs={'class': 'input', 'placeholder': 'phone'}),
            'address': TextInput(attrs={'class': 'input', 'placeholder': 'address'}),
            'city': Select(attrs={'class': 'input', 'placeholder': 'city'}, choices=CITY),
            'country': TextInput(attrs={'class': 'input', 'placeholder': 'country'}),
            'image': FileInput(attrs={'class': 'input', 'placeholder': 'image', }),
        }

