from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from rest_framework_simplejwt.authentication import JWTAuthentication

from django.core.files.base import ContentFile

from .models import Group

import base64

# Create your views here.


class CreateGroup(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        Group.objects.create(
            creator=request.user,
            name=request.data['name'],
            description=request.data['description'],
        )

        if "image_group" in request.data:
            format, imgstr = request.data['image_group'].split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr))
            file_name = str(request.user.id) + "_group" + "." + ext
            Group.objects.filter(creator=request.user).last().image_group.save(
                file_name, data, save=True
            )

        return Response(request.data)
