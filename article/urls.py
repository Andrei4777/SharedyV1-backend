from django.urls import path
from .views import (
    CreateArticle,
    TrendsArticle,
    SubscriptionArticle,
)

urlpatterns = [
    path('article', CreateArticle.as_view(), name="createArticle"),
    path('articles/trends', TrendsArticle.as_view(), name="trendsArticle"),
    path('articles/subscriptions', SubscriptionArticle.as_view(), name="subscriptionArticle"),
]
