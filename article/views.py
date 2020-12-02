from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from rest_framework_simplejwt.authentication import JWTAuthentication

from django.core.files.base import ContentFile

from .models import Tags, Article
from group.models import Group

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
