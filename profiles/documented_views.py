from profiles import views, serializers
from rest_framework import status
from rest_framework.authtoken import serializers as auth_serializer
from drf_yasg.utils import swagger_auto_schema

account_view = swagger_auto_schema(
    method="post",
    request_body=serializers.UserAccountSerializer,
    responses={status.HTTP_201_CREATED: serializers.UserAccountSerializer},
    operation_summary="Create user accounts.",
    operation_description="User account creation without any verification of credentials",
)(views.Account.as_view())

auth_token_view = swagger_auto_schema(
    method="post",
    request_body=auth_serializer.AuthTokenSerializer,
    responses={status.HTTP_200_OK: serializers.AuthTokenResponseSerializer},
    operation_summary="Obtain authentication token.",
)(views.LoginAuthToken.as_view())
