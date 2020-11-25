from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import RegistrerSerializer
from user.models import CustomUser

# Create your views here.


class CreateUser(APIView):
    def post(self, request, format=None):
        serializer = RegistrerSerializer(data=request.data)

        if serializer.is_valid():
            CustomUser.objects.create_user(
                request.data['username'],
                request.data['email'],
                request.data['password']
            )
            return Response("done")
        return Response("pasz valide")
