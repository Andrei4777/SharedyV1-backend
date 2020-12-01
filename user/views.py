from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView

from rest_framework_simplejwt.authentication import JWTAuthentication

from user.models import CustomUser
from .forms import RegistrationForm
from .serializers import UserSerializer
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
