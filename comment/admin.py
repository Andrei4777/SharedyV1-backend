from django.contrib import admin

from .models import Comment, LikeComment

# Register your models here.

admin.site.register(Comment)
admin.site.register(LikeComment)
