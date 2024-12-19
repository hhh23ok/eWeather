from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from notifications.models import BotUser


# Form to collect or update Telegram username
class TelegramUsernameForm(forms.ModelForm):
    class Meta:
        model = BotUser
        fields = ['username']
        labels = {'username': 'Telegram Username'}
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control',
                                               'placeholder': 'Enter Telegram Username'}),
        }


class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
