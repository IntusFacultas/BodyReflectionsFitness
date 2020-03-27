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
            user_token_exists = Token.objects.filter(
                user=request.user).exists()
            user_token_matches_request = request.COOKIES.get(
                settings.AUTH_HTTP_COOKIE) == request.user.auth_token.key
            token_not_expired = request.user.auth_token.created + \
                settings.AUTH_HTTP_COOKIE_EXPIRY > timezone.now()
            return user_token_exists and token_not_expired and user_token_matches_request
        return False

    def has_permission(self, request, view):
        return self.test_token_validity(request)
