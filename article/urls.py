from django.urls import path
from .views import (
    CreateArticle,
)

urlpatterns = [
    path('article', CreateArticle.as_view(), name="createArticle"),
]
