from profiles.views import Logout
from django.urls import path
from profiles import documented_views


urlpatterns = [
    path("login/", documented_views.auth_token_view, name="login"),
    path("logout/", Logout.as_view(), name="logout"),
    path("account/", documented_views.account_view, name="user_account"),
]
