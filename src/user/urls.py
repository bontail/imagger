from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from user.views import CreateUserView


urlpatterns = [
    path('register/', CreateUserView.as_view()),
    path('login/', TokenObtainPairView.as_view()),
    path('refresh_token/', TokenRefreshView.as_view()),
]
