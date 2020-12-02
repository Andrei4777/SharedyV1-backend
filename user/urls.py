from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from .views import (
    RandomUser,
    MyProfile,
    Profile,
    SearchUser,
    FollowersUser,
    EditUser,
)

from .views import CreateUser

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify', TokenVerifyView.as_view(), name="verify"),
    path('registrer/', CreateUser.as_view(), name="registrer"),
    path('users/random', RandomUser.as_view(), name="userRandom"),
    path('user/myprofile', MyProfile.as_view(), name="myprofile"),
    path('user/profile/<int:idUser>', Profile.as_view(), name="profile"),
    path('users/search/<str:user>', SearchUser.as_view(), name="search"),
    path('users/followers/<int:idUser>', FollowersUser.as_view(), name="followers"),
    path('user/edit', EditUser.as_view(), name="edit"),
]
