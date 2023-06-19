from django.urls import path
from registration.api.views import RegisterView, LoginView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path("auth/register/", RegisterView.as_view()),
    path("auth/login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("auth/refresh_token/", TokenRefreshView.as_view(), name="token_refresh"),
    path("auth/logincognito/", LoginView.as_view(), name="login_cognito"),
]
