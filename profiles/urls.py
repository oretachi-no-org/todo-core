from rest_framework.authtoken import views
from .views import Logout
from django.urls import path

urlpatterns = [
    path("login/", views.obtain_auth_token, name="login"),
    path("logout/", Logout.as_view(), name="logout")
]
