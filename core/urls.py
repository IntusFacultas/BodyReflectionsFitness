# core/urls.py

from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from rest_framework import routers
from core.views import UserViewSet, ExerciseViewSet

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r"exercises", ExerciseViewSet)
urlpatterns = [
    path('', include(router.urls)),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
