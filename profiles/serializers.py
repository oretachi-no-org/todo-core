from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.validators import ASCIIUsernameValidator
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password


class AuthTokenResponseSerializer(serializers.Serializer):
    token = serializers.CharField()

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


class UserAccountSerializer(serializers.Serializer):
    """
    Serializes a user account
    """

    email = serializers.EmailField(allow_blank=False)
    username = serializers.CharField(
        max_length=20,
        min_length=3,
        validators=[
            ASCIIUsernameValidator(),
            UniqueValidator(
                queryset=get_user_model().objects.all(),
                message="Username already taken",
            ),
        ],
    )
    first_name = serializers.CharField(max_length=25, allow_blank=True, default="")
    last_name = serializers.CharField(max_length=25, allow_blank=True, default="")
    password = serializers.CharField(min_length=9, max_length=35)

    def validate(self, data):
        """
        Validate secure password.
        """
        user_model = get_user_model()
        user = user_model(
            username=data.get("username", ""),
            email=data.get("email", ""),
            first_name=data.get("first_name", ""),
            last_name=data.get("last_name", ""),
        )

        validate_password(data.get("password", ""), user=user)
        return data

    def create(self, validated_data):
        user_model = get_user_model()
        user = user_model.objects.create_user(
            validated_data.get("username"),
            validated_data.get("email"),
            validated_data.get("password"),
        )
        user.first_name = validated_data.get("first_name", "")
        user.last_name = validated_data.get("last_name", "")
        user.save()
        return user

    def update(self, instance, validated_data):
        return validated_data
