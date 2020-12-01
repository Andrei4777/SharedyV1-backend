from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView

from rest_framework_simplejwt.authentication import JWTAuthentication

from article.models import LikeArticle, Article
from user.models import CustomUser, Subscription
from .forms import RegistrationForm
from .serializers import UserSerializer, MyUserSerializer
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
        user = CustomUser.objects.get(
            id=self.kwargs['idUser']
        )
        queryset = CustomUser.objects.filter(id=user.id)
        articles = Article.objects.filter(creator=user)

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
