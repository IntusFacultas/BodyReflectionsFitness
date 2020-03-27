from django.urls import path
from rest_framework import routers
from apiauth.views import TokenLogout, TokenLogin, CreateAccount, VerifySession
app_name = "api-auth"
router = routers.DefaultRouter()
urlpatterns = [
    path("verify-session/", VerifySession.as_view(), name="verify-session"),
    path("logout/", TokenLogout.as_view(), name="logout"),
    path("login/", TokenLogin.as_view(), name="login"),
    path('signup/', CreateAccount.as_view(), name='signup'),
]
urlpatterns += router.urls
