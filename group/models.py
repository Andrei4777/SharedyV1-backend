from django.db import models

# Create your models here.


class Group(models.Model):
    name = models.CharField(max_length=80)
    description = models.CharField(max_length=250, blank=False)
    image_group = models.ImageField(upload_to='', default='')
