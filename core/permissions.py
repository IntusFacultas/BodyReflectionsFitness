from rest_framework.permissions import BasePermission
from django.conf import settings
from rest_framework.authtoken.models import Token
import datetime
from django.utils import timezone


class IsTokenAuthenticated(BasePermission):
    """
    Allows access only to authenticated users.
    """

    def test_token_validity(self, request):
        if settings.AUTH_HTTP_COOKIE in request.COOKIES:
            if Token.objects.filter(
                    key=request.COOKIES[settings.AUTH_HTTP_COOKIE]).exists():
                token = Token.objects.get(
                    key=request.COOKIES[settings.AUTH_HTTP_COOKIE])
                token_not_expired = token.created + \
                    settings.AUTH_HTTP_COOKIE_EXPIRY > timezone.now()
                return token_not_expired  # and user_token_matches_request
        return False

    def has_permission(self, request, view):
        return self.test_token_validity(request)
