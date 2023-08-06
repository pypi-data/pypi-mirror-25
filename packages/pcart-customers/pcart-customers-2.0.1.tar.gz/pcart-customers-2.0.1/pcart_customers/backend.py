from django.contrib.auth.backends import ModelBackend
from .models import User


class EmailOrPhoneBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        from django.db.models import Q
        try:
            user = User.objects.get(Q(email=username)|Q(phone=username))
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
        except User.DoesNotExist:
            pass
