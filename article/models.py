from django.db import models
from django.utils import timezone

from group.models import Group
from user.models import CustomUser
from .choices import LikeChoicesArticles

# Create your models here.


class Tags(models.Model):
    name = models.CharField(max_length=20, blank=False)


class Article(models.Model):
    title = models.CharField(max_length=50, blank=False)
    content_article = models.TextField(max_length=850, blank=False)
    tag_article = models.ManyToManyField(Tags, blank=True)
    image_article = models.ImageField(upload_to="", null=True, blank=True)
    group_article = models.ForeignKey(Group, null=True, blank=True, on_delete=models.CASCADE)
    creator = models.ForeignKey(CustomUser, null=False, blank=False, on_delete=models.CASCADE)
    date_article = models.DateTimeField(default=timezone.now)


class LikeArticle(models.Model):
    article_like = models.ForeignKey(Article, blank=False, on_delete=models.CASCADE)
    user_like = models.ForeignKey(CustomUser, blank=False, on_delete=models.CASCADE)
    date_like = models.DateTimeField(default=timezone.now)
    choices_like = models.CharField(max_length=40, choices=LikeChoicesArticles, null=False)
