from django.db import models
from django.utils import timezone

from user.models import CustomUser
from article.models import Article
from group.models import Group

# Create your models here.


class Notification(models.Model):
    user_giving = models.ForeignKey(
        CustomUser,
        blank=False,
        on_delete=models.CASCADE,
        related_name='user_giving_notification',
    )
    user_receiving = models.ForeignKey(
        CustomUser,
        blank=False,
        on_delete=models.CASCADE,
        related_name='user_receiving_notification',
    )
    date_notification = models.DateTimeField(default=timezone.now)
    content_notification = models.TextField(default="")
    article = models.ForeignKey(Article, blank=True, null=True, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, blank=True, null=True, on_delete=models.CASCADE)
