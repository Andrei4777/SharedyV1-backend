from django.db import models
from django.utils import timezone

from user.models import CustomUser
from article.models import Article
from .choices import LikeChoicesComment

# Create your models here.


class Comment(models.Model):
    article_comment = models.ForeignKey(Article, blank=False, on_delete=models.CASCADE)
    content_comment = models.CharField(max_length=500, blank=False)
    date_comment = models.DateTimeField(default=timezone.now)
    user_comment = models.ForeignKey(CustomUser, blank=False, on_delete=models.CASCADE)


class LikeComment(models.Model):
    user_like = models.ForeignKey(CustomUser, blank=False, on_delete=models.CASCADE)
    choices_like = models.CharField(max_length=40, choices=LikeChoicesComment, null=False)
    comment_like = models.ForeignKey(Comment, blank=False, on_delete=models.CASCADE)
