from rest_framework.views import APIView
from rest_framework import status, viewsets
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.conf import settings
from core.permissions import IsTokenAuthenticated
from core.serializers import UserSerializer, ExerciseSerializer
from core.models import Exercise
User = get_user_model()


class ExerciseViewSet(viewsets.ModelViewSet):
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer
    permission_classes = (IsTokenAuthenticated)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsTokenAuthenticated)
