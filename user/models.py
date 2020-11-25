from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class CustomUser(AbstractUser):
    image_profile = models.ImageField(upload_to='', default='user-default.png')
