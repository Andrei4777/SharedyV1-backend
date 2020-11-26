from django import forms
from django.utils.translation import gettext_lazy as _
from user.models import CustomUser
from django.contrib.auth import password_validation
from django.contrib.auth.forms import (
    UserCreationForm,
)

""" Manages registration form """


class RegistrationForm(UserCreationForm):
    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={'autocomplete': 'new-password', 'class': 'input_user', 'placeholder': 'Password'}
        ),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput(
            attrs={'autocomplete': 'new-password', 'class': 'input_user', 'placeholder': 'Confirm password'}
        ),
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
    )

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'input_user', 'placeholder': 'Username'}),
            'email': forms.EmailInput(attrs={'class': 'input_user', 'placeholder': 'Mail'}),
        }
