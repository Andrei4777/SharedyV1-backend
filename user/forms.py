from user.models import CustomUser
from django.contrib.auth.forms import (
    UserCreationForm,
)

""" Manages registration form """


class RegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')
