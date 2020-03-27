from django.urls import path, include
from rest_framework import routers
from core.views import UserViewSet, ExerciseViewSet

app_name = "core"

router = routers.DefaultRouter()
router.register(r'users', UserViewSet, basename="users")
router.register(r"exercises", ExerciseViewSet, basename="exercises")

urlpatterns = []
urlpatterns += router.urls
