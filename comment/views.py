from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView

from rest_framework_simplejwt.authentication import JWTAuthentication

from django.db.models import Count

from .models import Comment
from .serializers import CommentSerializer
from .paginations import CommentPagination

# Create your views here.


class CreateComment(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        Comment.objects.create(
            article_comment_id=request.data['idArticle'],
            content_comment=request.data['comment'],
            user_comment=request.user,
        )
        return Response("OK")


def formatComment(queryset):
    for i in queryset:
        i.infos_comment = {
            "creator": {
                "image_profile": str(i.user_comment.image_profile.url),
                "username": i.user_comment.username,
                "id": i.user_comment.id,
            },
            "like": i.likecomment_set.all().filter(
                choices_like=1
            ).count(),
            "dislike": i.likecomment_set.all().filter(
                choices_like=2
            ).count()
        }


class TrendsComment(ListAPIView):
    authentication_classes = [JWTAuthentication]
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = CommentPagination

    def get_queryset(self):
        queryset = Comment.objects.filter(
            article_comment_id=self.kwargs['idArticle']
        ).annotate(
            count=Count('likecomment')
        ).order_by('-count')

        formatComment(queryset)

        return queryset


class RecentComment(ListAPIView):
    authentication_classes = [JWTAuthentication]
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = CommentPagination

    def get_queryset(self):
        queryset = Comment.objects.filter(
            article_comment_id=self.kwargs['idArticle']
        ).order_by('-date_comment')

        formatComment(queryset)

        return queryset


class OldComment(ListAPIView):
    authentication_classes = [JWTAuthentication]
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = CommentPagination

    def get_queryset(self):
        queryset = Comment.objects.filter(
            article_comment_id=self.kwargs['idArticle']
        ).order_by('date_comment')

        formatComment(queryset)

        return queryset
