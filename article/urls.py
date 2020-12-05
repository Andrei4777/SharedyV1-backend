from django.urls import path
from .views import (
    CreateArticle,
    TrendsArticle,
    SubscriptionArticle,
    UserArticle,
    GroupArticle,
    TagArticle,
    LikesArticle,
)

urlpatterns = [
    path('article', CreateArticle.as_view(), name="createArticle"),
    path('articles/trends', TrendsArticle.as_view(), name="trendsArticle"),
    path('articles/subscriptions', SubscriptionArticle.as_view(), name="subscriptionArticle"),
    path('articles/user/<int:idUser>', UserArticle.as_view(), name="articleUser"),
    path('articles/group/<int:idArticle>', GroupArticle.as_view(), name="articleGroup"),
    path('articles/tag/<int:idTag>', TagArticle.as_view(), name="articleTag"),
    path('article/likes', LikesArticle.as_view(), name="articleLike"),
]
