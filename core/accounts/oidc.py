from django.core.exceptions import PermissionDenied
from mozilla_django_oidc.auth import OIDCAuthenticationBackend

from accounts.models import User


class CustomOIDCAuthenticationBackend(OIDCAuthenticationBackend):
    def filter_users_by_claims(self, claims):
        """فقط با national_code کاربر را پیدا کن."""
        national_code = claims.get('national_code')
        if not national_code:
            return self.UserModel.objects.none()
        return self.UserModel.objects.filter(national_code=national_code)

    def create_user(self, claims):
        """کاربر جدید ساخته نمی‌شود؛ خطا برگردان."""
        raise PermissionDenied("کاربر وجود نداشت. با پشتیبانی تماس بگیرید.")

    def verify_claims(self, claims):
        """فقط وجود national_code را بررسی کن."""
        return 'national_code' in claims