from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class LoginUserForm(AuthenticationForm):  # inheritance from standard user authentication on site
    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-input'}))


class SecretTokenForm(UserCreationForm):
    password = forms.CharField(label='Secret Token from Telegram Bot',
                               widget=forms.TextInput(attrs={'class': 'form-input'}))


class PasswordReset(UserCreationForm):
    login_or_email = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-input'}))


class ChangeEmail(UserCreationForm):
    new_email = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-input'}))


class PasswordResetForUser(UserCreationForm):
    new_password = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-input'}))


class RegisterForm(UserCreationForm):
    username = forms.CharField(label='Username', widget=forms.TextInput(), max_length=100, initial='')
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1')
