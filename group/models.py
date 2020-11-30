from django.db import models

from user.models import CustomUser

# Create your models here.


class Group(models.Model):
    creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=80)
    description = models.CharField(max_length=250, blank=False)
    image_group = models.ImageField(upload_to='', default='group-default.svg.png')
    followers = models.ManyToManyField(CustomUser, related_name="group_followers")
