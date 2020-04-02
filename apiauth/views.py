from django.http import HttpResponse
from django.utils import timezone
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from rest_framework import parsers, renderers, status
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.schemas import coreapi as coreapi_schema, ManualSchema
from rest_framework.authtoken.models import Token
from rest_framework.compat import coreapi, coreschema
from rest_framework.response import Response
from rest_framework.views import APIView
from core.permissions import IsTokenAuthenticated
from django.conf import settings
from apiauth.forms import ProfileForm
from .serializers import AccountSerializer
import datetime


@method_decorator(csrf_exempt, name='dispatch')
class TokenLogin(APIView):
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (
        parsers.FormParser,
        parsers.MultiPartParser, parsers.JSONParser,
    )
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class = AuthTokenSerializer

    if coreapi_schema.is_enabled():
        schema = ManualSchema(
            fields=[
                coreapi.Field(
                    name="username",
                    required=True,
                    location='form',
                    schema=coreschema.String(
                        title="Username",
                        description="Valid username for authentication",
                    ),
                ),
                coreapi.Field(
                    name="password",
                    required=True,
                    location='form',
                    schema=coreschema.String(
                        title="Password",
                        description="Valid password for authentication",
                    ),
                ),
            ],
            encoding="application/json",
        )

    def get_serializer_context(self):
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self
        }

    def get_serializer(self, *args, **kwargs):
        kwargs['context'] = self.get_serializer_context()
        return self.serializer_class(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        user.last_login = timezone.now()
        Token.objects.get(user=user).delete()
        token = Token.objects.create(user=user)
        token, created = Token.objects.get_or_create(user=user)
        response = Response(status=status.HTTP_200_OK)
        response.set_cookie(
            settings.AUTH_HTTP_COOKIE,
            token.key, expires=timezone.now() + datetime.timedelta(days=1),
            secure=settings.SESSION_COOKIE_SECURE,
            httponly=True,
            samesite=True
        )
        # response.cookies[settings.AUTH_HTTP_COOKIE]['httponly'] = True
        return response


class VerifySession(APIView):
    permission_classes = (IsTokenAuthenticated,)

    def get(self, request):
        token = Token.objects.get(
            key=request.COOKIES[settings.AUTH_HTTP_COOKIE])
        profile = token.user.profile
        account_data = AccountSerializer(instance=profile).data
        return Response(data=account_data, status=status.HTTP_200_OK)


@method_decorator(csrf_exempt, name='dispatch')
class ChangePassword(APIView):
    permission_classes = (IsTokenAuthenticated,)

    def post(self, request):
        token = Token.objects.get(
            key=request.COOKIES[settings.AUTH_HTTP_COOKIE])
        user = token.user
        form = PasswordChangeForm(user, request.data)
        if form.is_valid():
            form.save()
            return Response(status=status.HTTP_200_OK)
        return Response(
            data={"errors": form.errors.as_json()},
            status=status.HTTP_400_BAD_REQUEST
        )


@method_decorator(csrf_exempt, name='dispatch')
class CreateAccount(APIView):
    def post(self, request):
        account_form = UserCreationForm(
            data=request.data.get("accountInformation"))
        profile_form = ProfileForm(data=request.data.get("profileInformation"))
        if account_form.is_valid() and profile_form.is_valid():
            user = account_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            return Response(status=status.HTTP_200_OK)
        elif account_form.is_valid():
            return Response(
                data={
                    "profileErrors": profile_form.errors.as_json(),
                    "accountErrors": {}
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        elif profile_form.is_valid():
            return Response(
                data={
                    "profileErrors": {},
                    "accountErrors": account_form.errors.as_json()
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        else:
            return Response(
                data={
                    "profileErrors": profile_form.errors.as_json(),
                    "accountErrors": account_form.errors.as_json()
                },
                status=status.HTTP_400_BAD_REQUEST
            )


class TokenLogout(APIView):
    permission_classes = (IsTokenAuthenticated,)

    def get(self, request):
        try:
            token = Token.objects.get(
                key=request.COOKIES[settings.AUTH_HTTP_COOKIE])
            token.delete()
            return Response(status=status.HTTP_200_OK)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)
