from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.serializers import ValidationError
from profiles.serializers import UserAccountSerializer


class TestUserAccountSerizalizer(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="testuser", email="test@test.com", password="pass"
        )
        cls.user.first_name = "John"
        cls.user.last_name = "Wick"
        cls.user.save()

    def test_valid(self):
        serializer = UserAccountSerializer(
            data={
                "username": "test",
                "email": "test@testing.com",
                "password": "strong_password_for_a_test",
            }
        )

        self.assertTrue(serializer.is_valid(raise_exception=True))

    def test_weak_password(self):
        serializer = UserAccountSerializer(
            data={
                "username": "test",
                "email": "test@testing.com",
                "password": "password",
            }
        )
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_duplicate_username(self):
        serializer = UserAccountSerializer(
            data={
                "username": "testuser",
                "email": "unknown@user.com",
                "password": "this_is a strongPasswerd",
            }
        )
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_user_create(self):
        serializer = UserAccountSerializer(
            data={
                "username": "unknown",
                "email": "testuser@unknown.com",
                "password": "strongest password in the world",
                "first_name": "Darth",
                "last_name": "Vader",
            }
        )

        self.assertTrue(serializer.is_valid())
        user = serializer.save()

        self.assertEqual(user.first_name, "Darth")
