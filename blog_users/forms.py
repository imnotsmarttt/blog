from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm

from .models import CustomUser


class UserRegisterForm(UserCreationForm):
    """Форма регистрации пользователя"""
    password1 = forms.CharField(
        label='',
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'new-password', 'class': 'form_input', 'placeholder': 'Введите пароль'}),
    )
    password2 = forms.CharField(
        label='',
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'new-password', 'class': 'form_input', 'placeholder': 'Повторите пароль'}),
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'password1', 'password2', 'country', 'region']
        labels = {
            'username': '',
            'first_name': '',
            'last_name': '',
            'country': '',
            'region': '',
        }

        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form_input', 'placeholder': 'Введите логин'
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'form_input', 'placeholder': 'Введите имя'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form_input', 'placeholder': 'Введите фамилию'
            }),
            'country': forms.TextInput(attrs={
                'class': 'form_input', 'placeholder': 'Страна'
            }),
            'region': forms.TextInput(attrs={
                'class': 'form_input', 'placeholder': 'Регион'
            }),
        }


class UserAuthForm(AuthenticationForm):
    username = forms.CharField(label='', widget=forms.TextInput(attrs={
        'autofocus': True, 'class': 'form_input', 'placeholder': 'Введите логин'}))
    password = forms.CharField(
        label='',
        strip=False,
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'current-password', 'class': 'form_input', 'placeholder': 'Введите логин'}),
    )
