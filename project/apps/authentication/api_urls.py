from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from apps.authentication.views import LoginView, LogoutView, RegisterView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="api-register"),
    path("login/", LoginView.as_view(), name="api-login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="api-token-refresh"),
    path("logout/", LogoutView.as_view(), name="api-logout"),
]
