from django.contrib.auth.backends import BaseBackend
from django.db.models import Q
from user.models import User


class CustomBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        login_identifier = username
        if not login_identifier or not password:
            return None
        try:
            user = User.objects.get(
                Q(username=login_identifier) | Q(email__iexact=login_identifier)
            )
        except (User.DoesNotExist, User.MultipleObjectsReturned):
            return None

        if user.check_password(password) and user.is_active:
            return user
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None


