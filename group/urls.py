from django.urls import path

from .views import (
    CreateGroup,
    GroupsFollow,
    GroupTrends,
    MyGroups,
    GroupOnly,
    GroupFollow,
)


urlpatterns = [
    path('group', CreateGroup.as_view(), name="createGroup"),
    path('groups/follow', GroupsFollow.as_view(), name="groupFollow"),
    path('groups/trends', GroupTrends.as_view(), name="groupTrends"),
    path('groups/mygroups', MyGroups.as_view(), name="myGroups"),
    path('group/only/<int:idGroup>', GroupOnly.as_view(), name="onlyGroup"),
    path('group/follow', GroupFollow.as_view(), name="groupFollow"),
]
