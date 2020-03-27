from core.serializers import UserSerializer, ExerciseSerializer
from django.contrib.auth import get_user_model
from core.models import Exercise
from rest_framework import viewsets
User = get_user_model()


class ExerciseViewSet(viewsets.ModelViewSet):
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
