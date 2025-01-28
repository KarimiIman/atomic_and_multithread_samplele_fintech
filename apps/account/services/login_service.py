from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.cache import cache
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class UserLoginService:

    def __init__(self, email=None,password=None) -> None:
        self.email = email
        self.password = password

    def login(self):
        if not self._check_user_exist():
            return False, "User must register first"
        return self._user_login()

    def _user_login(self):
        """
        we can add extera senario for login (otp, login with username , phone number and etc.)
        """
        if self.email and self.password:
            return self._login_with_email_and_password()
        return False, "No valid login scenario met. Please try again or contact support."

    def _login_with_email_and_password(self):
        user = User.objects.get(email=self.email)
        if user.check_password(self.password):
            return self._generate_tokens(user)
        return False, 'Invalid email or password'

    def _generate_tokens(self, user):
        token_obj = RefreshToken.for_user(user)
        return True, {
            'access_token': str(token_obj.access_token),
            'refresh_token': str(token_obj),
            'username': user.username,
            'user_id': user.id,
            'role': "badan ezafe konam",
        }

    def _check_user_exist(self) -> bool:
        if not (self.email):
            return False
        return User.objects.filter(
            email=self.email, is_active=True
        ).exists()