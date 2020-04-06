from django.urls import path
from rest_framework import routers
from apiauth.views import (
    TokenLogout, TokenLogin,
    CreateAccount, VerifySession,
    ChangePassword, UpdateProfile
)
app_name = "api-auth"
router = routers.DefaultRouter()
urlpatterns = [
    path("update-profile/", UpdateProfile.as_view(), name="update-profile"),
    path("change-password/", ChangePassword.as_view(), name="change-password"),
    path("verify-session/", VerifySession.as_view(), name="verify-session"),
    path("logout/", TokenLogout.as_view(), name="logout"),
    path("login/", TokenLogin.as_view(), name="login"),
    path('signup/', CreateAccount.as_view(), name='signup'),
]
urlpatterns += router.urls
