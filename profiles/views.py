from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework import status
from rest_framework.settings import api_settings
from django.contrib.auth import logout
from profiles.serializers import UserAccountSerializer


class Logout(APIView):
    """
    View to logout
    """

    def delete(self, request, format=None):
        request.user.auth_token.delete()
        logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)


class LoginAuthToken(ObtainAuthToken):
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class Account(APIView):
    """
    Create, delete and update accounts.
    """

    def post(self, request, format=None) -> Response:
        """
        Creates a new user.
        """
        serializer = UserAccountSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
