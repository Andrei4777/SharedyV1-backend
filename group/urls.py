from django.urls import path

from .views import CreateGroup


urlpatterns = [
    path('group', CreateGroup.as_view(), name="create group"),
]
