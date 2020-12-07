from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView

from rest_framework_simplejwt.authentication import JWTAuthentication

from django.core.files.base import ContentFile
from django.db.models import Count

from .models import Group
from .serializers import GroupFollowSerializer
from .paginations import GroupPagination

from user.models import CustomUser


import base64

# Create your views here.

""" Views to create a group """


class CreateGroup(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        new_group = Group.objects.create(
            creator=request.user,
            name=request.data['name'],
            description=request.data['description'],
        )

        if "image_group" in request.data:
            format, imgstr = request.data['image_group'].split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr))
            file_name = str(request.user.id) + "_group" + "." + ext
            new_group.image_group.save(
                file_name, data, save=True
            )

        return Response("OK")


""" Views to get all group that we follow """


class GroupsFollow(ListAPIView):
    authentication_classes = [JWTAuthentication]
    serializer_class = GroupFollowSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = GroupPagination

    def get_queryset(self):
        queryset = Group.objects.filter(
            followers__id=self.request.user.id
        ).order_by('name')

        for i in queryset:
            i.infos_user = {
                "username": CustomUser.objects.get(
                    id=i.creator.id
                ).username
            }
        return queryset


""" Views to get all group with more followers """


class GroupTrends(ListAPIView):
    authentication_classes = [JWTAuthentication]
    serializer_class = GroupFollowSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = GroupPagination

    def get_queryset(self):
        queryset = Group.objects.annotate(countFollow=Count(
            "followers"
        )).order_by("-countFollow")

        for i in queryset:
            i.infos_user = {
                "username": CustomUser.objects.get(
                    id=i.creator.id
                ).username
            }

        return queryset


""" Views To get all group that belongs to me """


class MyGroups(ListAPIView):
    authentication_classes = [JWTAuthentication]
    serializer_class = GroupFollowSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = GroupPagination

    def get_queryset(self):
        queryset = Group.objects.filter(
            creator=self.request.user
        )

        for i in queryset:
            i.infos_user = {
                "username": CustomUser.objects.get(
                    id=i.creator.id
                ).username
            }

        return queryset


""" views to get informations to a group """


class GroupOnly(ListAPIView):
    authentication_classes = [JWTAuthentication]
    serializer_class = GroupFollowSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = GroupPagination

    def get_queryset(self):
        queryset = Group.objects.filter(
            id=self.kwargs['idGroup']
        )

        for i in queryset:
            i.infos_user = {
                "username": i.creator.username,
            }

        return queryset
