from django.test import TestCase
from django.db.utils import IntegrityError
from django.contrib.auth import get_user_model


class TestUserModel(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user("testuser", "test@test.com", "testpass")

    def test_duplicate_user(self):
        with self.assertRaises(IntegrityError):
            get_user_model().objects.create_user(
                self.user.get_username(), "test@test.com", "testpass"
            )
