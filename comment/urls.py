from django.urls import path

from .views import (
    CreateComment,
    TrendsComment,
    RecentComment,
    OldComment,
)

urlpatterns = [
    path('comment', CreateComment.as_view(), name="comment"),
    path('comments/<int:idArticle>/trends', TrendsComment.as_view(), name="trendsComment"),
    path('comments/<int:idArticle>/recent', RecentComment.as_view(), name="recentComment"),
    path('comments/<int:idArticle>/old', OldComment.as_view(), name="oldComment"),
]
