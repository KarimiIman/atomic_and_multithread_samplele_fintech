from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from apps.account.views import UserLoginApiView

urlpatterns = [
    path('login', UserLoginApiView.as_view(), name='user_login_api'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]