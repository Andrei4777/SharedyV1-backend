from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class CustomUser(AbstractUser):
    image_profile = models.ImageField(upload_to='', default='user-default.svg.png')
    description = models.TextField(
        max_length=125,
        default="Hello, I am a happy young user who wish to browse the temple of ideas on shaready.fr."
    )
