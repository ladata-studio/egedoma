from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

class PasswordlessAuthBackend(ModelBackend):
    def authenticate(self, request, telegram_id):
        User = get_user_model()
        try:
            user = User.objects.get(telegram_id=telegram_id)
            return user
        except User.DoesNotExist:
            return None

    def get_user(self, telegram_id):
        User = get_user_model()
        try:
            return User.objects.get(telegram_id=telegram_id)
        except User.DoesNotExist:
            return None
