from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView

from rest_framework_simplejwt.authentication import JWTAuthentication

from django.core.files.base import ContentFile
from django.db.models import Count

from .models import Tags, Article, LikeArticle
from .serializers import ArticleSerializer
from .paginations import ArticlePagination
from group.models import Group
from comment.models import Comment
from user.models import Subscription

from datetime import datetime, timedelta
import base64

# Create your views here.


class CreateArticle(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        article = Article.objects.create(
            title=request.data["title"],
            content_article=request.data["content"],
            creator=request.user
        )

        if len(request.data["tags"]) != 0:
            for i in request.data["tags"]:
                tags_is_exist = Tags.objects.filter(
                    name=i
                ).count()
                if tags_is_exist == 0:
                    Tags.objects.create(
                        name=i
                    )
            tags = Tags.objects.filter(
                name__in=request.data["tags"]
            )
            article.tag_article.add(*tags)
        if request.data["groups"] != "Add in group":
            article.group_article = Group.objects.get(
                name=request.data["groups"]
            )

        if request.data["imageArticle"]:
            format, imgstr = request.data['imageArticle'].split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr))
            file_name = str(article.id) + "_article" + "." + ext
            article.image_article.save(
                file_name, data, save=True
            )
        return Response("OK")


def formatDataArticle(queryset, user):
    for i in queryset:
        i.infos_article = {
            "nbs_gold_like": LikeArticle.objects.filter(
                article_like=i,
                choices_like=1,
            ).count(),
            "nbs_like": LikeArticle.objects.filter(
                article_like=i,
                choices_like=2,
            ).count(),
            "nbs_dislike": LikeArticle.objects.filter(
                article_like=i,
                choices_like=3,
            ).count(),
            "nbs_comment": Comment.objects.filter(
                article_comment=i,
            ).count(),
            "creator": {
                "username": i.creator.username,
                "image_profile": str(i.creator.image_profile),
            },
        }

        if i.likearticle_set.filter(user_like=user).count():
            i.infos_article["liked"] = i.likearticle_set.filter(
                user_like=user,
            )[0].choices_like
        if i.group_article is not None:
            i.infos_article["groups"] = {
                "id": i.group_article.id,
                "name": i.group_article.name
            }


class TrendsArticle(ListAPIView):
    authentication_classes = [JWTAuthentication]
    serializer_class = ArticleSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = ArticlePagination

    def get_queryset(self):
        last_month = datetime.today() - timedelta(days=30)
        queryset = Article.objects.filter(
            date_article__gte=last_month
        ).annotate(
            count=Count('likearticle')
        ).order_by('-count')

        formatDataArticle(queryset, self.request.user)

        return queryset


class SubscriptionArticle(ListAPIView):
    authentication_classes = [JWTAuthentication]
    serializer_class = ArticleSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = ArticlePagination

    def get_queryset(self):
        all_follow = Subscription.objects.filter(
            id_giving=self.request.user
        )
        list_follow = [i.id_receiving for i in all_follow]
        queryset = Article.objects.filter(
            creator__in=list_follow
        ).order_by('-date_article')
        formatDataArticle(queryset, self.request.user)

        return queryset


class UserArticle(ListAPIView):
    authentication_classes = [JWTAuthentication]
    serializer_class = ArticleSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = ArticlePagination

    def get_queryset(self):
        if self.kwargs['idUser'] > 0:
            idUser = self.kwargs['idUser']
        else:
            idUser = self.request.user.id
        queryset = Article.objects.filter(
            creator__id=idUser
        ).order_by('-date_article')
        formatDataArticle(queryset, self.request.user)

        return queryset


class GroupArticle(ListAPIView):
    authentication_classes = [JWTAuthentication]
    serializer_class = ArticleSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = ArticlePagination

    def get_queryset(self):
        queryset = Article.objects.filter(
            group_article__id=self.kwargs['idArticle']
        ).order_by('-date_article')
        formatDataArticle(queryset, self.request.user)

        return queryset


class TagArticle(ListAPIView):
    authentication_classes = [JWTAuthentication]
    serializer_class = ArticleSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = ArticlePagination

    def get_queryset(self):
        queryset = Article.objects.filter(
            tag_article__id=self.kwargs['idTag']
        ).order_by('-date_article')
        formatDataArticle(queryset, self.request.user)

        return queryset
