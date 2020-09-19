from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import RequestsClient


class LoginTest(APITestCase):
    """
    Unit tests for User login
    """

    @classmethod
    def setUpTestData(cls):
        """
        Create user in database
        """
        cls.user = User.objects.create_user(
            "testuser", "testuser@test.com", "testingpass"
        )
        cls.user.first_name = "John"
        cls.user.last_name = "Wick"
        cls.user.save()

    def test_user_names(self):
        user = User.objects.get_by_natural_key("testuser")

        self.assertEqual(user.first_name, self.user.first_name)

    def test_login_post(self):
        url = reverse("login")
        login_response = self.client.post(
            url,
            {"username": "testuser", "password": "testingpass"},
        )
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)
        self.assertContains(login_response, "token")

    def test_wrong_login(self):
        url = reverse("login")
        response = self.client.post(url, {"username": "testuser", "password": "hacker"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_req(self):
        url = reverse("login")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


class TestLogout(APITestCase):
    """
    Unit tests for user logout
    """

    @classmethod
    def setUpTestData(cls):
        """
        Create user in database
        """
        cls.user = User.objects.create_user(
            "testuser", "testuser@test.com", "testingpass"
        )
        cls.user.first_name = "John"
        cls.user.last_name = "Wick"
        cls.user.save()

    def test_logout(self):
        login_url = reverse("login")
        logout_url = reverse("logout")
        response = self.client.post(
            login_url, {"username": "testuser", "password": "testingpass"}
        )
        token = response.data.get("token")
        response_again = self.client.post(
            login_url, {"username": "testuser", "password": "testingpass"}
        )
        token_again = response_again.data.get("token")
        self.assertEqual(token, token_again)
        self.client.login(username="testuser", password="testingpass")
        self.client.delete(logout_url)
        new_response = self.client.post(
            login_url, {"username": "testuser", "password": "testingpass"}
        )
        new_token = new_response.data.get("token")
        self.assertNotEqual(token, new_token)


class TestUserCreate(APITestCase):
    """
    Unit tests for create user.
    """

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            "testuser", "test@test.com", "strong-passwert43:"
        )
        cls.user.first_name = "Pink"
        cls.user.last_name = "Panther"
        cls.user.save()

        cls.url = reverse("user_account")

    def test_create_new_user(self):
        response = self.client.post(
            self.url,
            {
                "username": "amazing_user",
                "email": "amazing@user.com",
                "password": "very_strong_pesswort32",
                "firstName": "Shazam",
            },
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get("first_name"), "Shazam")
