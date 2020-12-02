from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView

from rest_framework_simplejwt.authentication import JWTAuthentication

from django.core.files.base import ContentFile

from article.models import LikeArticle, Article
from user.models import CustomUser, Subscription
from .forms import RegistrationForm
from .serializers import UserSerializer, MyUserSerializer, FollowersSerializer
from .paginations import UserPagination

import base64

# Create your views here.


class CreateUser(APIView):
    def post(self, request, format=None):
        form = RegistrationForm(data=request.data)

        if form.is_valid():
            CustomUser.objects.create_user(
                username=request.data['username'],
                email=request.data['email'],
                password=request.data['password1']
            )
            return Response("OK")
        else:
            return Response(form.errors.as_data())


""" Views to get 20 users random in apllication """


class RandomUser(ListAPIView):
    authentication_classes = [JWTAuthentication]
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = UserPagination

    def get_queryset(self):
        queryset = CustomUser.objects.order_by("?")

        return queryset


""" view to take all the information of the connected users. """


class MyProfile(ListAPIView):
    authentication_classes = [JWTAuthentication]
    serializer_class = MyUserSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = CustomUser.objects.filter(id=self.request.user.id)
        articles = Article.objects.filter(creator=self.request.user)

        for i in queryset:
            i.infos_user = {
                "nbs_follow": Subscription.objects.filter(
                    id_receiving=self.request.user.id
                ).count(),
                "nbs_goldLike": LikeArticle.objects.filter(
                    article_like__in=articles,
                    choices_like=1
                ).count()
            }
        return queryset


""" view to take all informations of the user """


class Profile(ListAPIView):
    authentication_classes = [JWTAuthentication]
    serializer_class = MyUserSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = CustomUser.objects.filter(id=self.kwargs['idUser'])
        articles = Article.objects.filter(creator=self.kwargs['idUser'])

        for i in queryset:
            i.infos_user = {
                "nbs_follow": Subscription.objects.filter(
                    id_receiving=self.kwargs['idUser']
                ).count(),
                "nbs_goldLike": LikeArticle.objects.filter(
                    article_like__in=articles,
                    choices_like=1
                ).count()
            }
        return queryset


""" views to get informations searched of user """


class SearchUser(ListAPIView):
    authentication_classes = [JWTAuthentication]
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = CustomUser.objects.filter(
            username__icontains=self.kwargs['user']
        )[:20]

        return queryset


""" views to get all followers of a user """


class FollowersUser(ListAPIView):
    authentication_classes = [JWTAuthentication]
    serializer_class = FollowersSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = UserPagination

    def get_queryset(self):
        if self.kwargs.get("idUser") == 0:
            idUser = self.request.user.id
        else:
            idUser = self.kwargs.get("idUser")

        queryset = CustomUser.objects.get(
            id=idUser
        ).user_receiving_follow.all()

        for i in queryset:
            serializer = UserSerializer(
                CustomUser.objects.get(
                    id=i.id_giving.id
                )
            )
            i.infos_user = serializer.data

        return queryset


""" views to edit profile """


class EditUser(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        serializer = UserSerializer(
            CustomUser.objects.get(
                id=request.user.id
            )
        )

        return Response(serializer.data)

    def post(self, request, format=None):
        request.user.description = request.data['description']
        request.user.username = request.data['username']

        if "image_profile" in request.data:
            format, imgstr = request.data['image_profile'].split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr))
            file_name = str(request.user.id) + "img_profile" + "." + ext
            if request.user.image_profile != "user-default.svg.png":
                request.user.image_profile.delete(save=True)

            request.user.image_profile.save(
                file_name, data, save=True
            )

        request.user.save()
        return Response("OK")
