from rest_framework.views import APIView
from rest_framework.response import Response

from user.models import CustomUser
from .forms import RegistrationForm

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
