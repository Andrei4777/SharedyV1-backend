from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView

from rest_framework_simplejwt.authentication import JWTAuthentication

from article.models import LikeArticle, Article
from user.models import CustomUser, Subscription
from .forms import RegistrationForm
from .serializers import UserSerializer, MyUserSerializer, FollowersSerializer
from .paginations import UserPagination

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
