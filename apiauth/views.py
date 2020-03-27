from django.http import HttpResponse
from django.utils import timezone
from django.views import View
from django.contrib.auth.forms import UserCreationForm
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
import datetime


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
        token, created = Token.objects.get_or_create(user=user)
        if not created:
            token.created = datetime.datetime.now()
        response = Response(status=status.HTTP_200_OK)
        response.set_cookie(
            settings.AUTH_HTTP_TOKEN,
            token.key, expires=timezone.now() + datetime.timedelta(days=1)
        )
        return response


class VerifySession(APIView):
    permission_classes = (IsTokenAuthenticated,)

    def get(self, request):
        return Response(status=status.HTTP_200_OK)


class CreateAccount(APIView):
    def post(self, request):
        account_form = UserCreationForm(request.POST.get("accountInformation"))
        profile_form = ProfileForm(request.POST.get("profileInformation"))
        if account_form.is_valid() and profile_form.is_valid():
            account_form.save()
            profile_form.save()
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

    def post(self, request):
        try:
            request.user.auth_token.delete()
            return Response(status=status.HTTP_200_OK)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)
