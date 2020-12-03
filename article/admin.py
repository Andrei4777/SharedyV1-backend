from django.contrib import admin
from .models import Article, Tags, LikeArticle

# Register your models here.

admin.site.register(Article)
admin.site.register(Tags)
admin.site.register(LikeArticle)
