from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status


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
