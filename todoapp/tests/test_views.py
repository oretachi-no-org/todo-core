from django.urls import reverse
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

from todoapp import models


class TestListViewSet(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.list_url = "/api/todo/lists/"
        user_model = get_user_model()
        cls.user = user_model.objects.create_user(
            "testuser", "test@test.com", "strong-passwert"
        )
        cls.user.first_name = "John"
        cls.user.last_name = "Snow"
        cls.user.save()

    def setUp(self) -> None:
        token_url = reverse("login")
        token_response = self.client.post(
            token_url, {"username": "testuser", "password": "strong-passwert"}
        )
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {token_response.data.get('token')}"
        )

        self.test_list = self.client.post(self.list_url, {"name": "Default"}).data
        self.temp_list_url = f"{self.list_url}{self.test_list.get('list_id')}/"

    def test_create_list(self):
        lists_response = self.client.post(self.list_url, {"name": "Test List"})
        list_id = lists_response.data.get("list_id")
        list_item: models.List = models.List.objects.get(list_id=list_id)
        self.assertEqual(list_item.owner.first_name, "John")

    def test_create_with_empty_name(self):
        list_response = self.client.post(self.list_url, {"name": ""})
        self.assertEqual(list_response.status_code, 400)

    def test_get_list_by_id(self):
        list_response = self.client.get(self.temp_list_url)
        self.assertEqual(list_response.status_code, 200)
        self.assertEqual(list_response.data.get("name"), "Default")

    def test_update_by_put(self):
        list_response = self.client.put(self.temp_list_url, {"name": "New Default"})

        self.assertEqual(list_response.data.get("name"), "New Default")

    def test_delete(self):
        delete_response = self.client.delete(self.temp_list_url)
        self.assertEqual(delete_response.status_code, 204)
        find_response = self.client.get(self.temp_list_url)
        self.assertEqual(find_response.status_code, 404)


class TestTaskViewSet(APITestCase):
    """
    Unit tests for TaskViewSet.
    """

    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            "hashirama", "senju@konoha.com", "testin_pa#@ sswo2rd$"
        )
        cls.user.first_name = "Hashirama"
        cls.user.last_name = "Senju"
        cls.user.save()
        cls.list_url = "/api/todo/lists/"

    def setUp(self) -> None:
        token_url = reverse("login")
        token_response = self.client.post(
            token_url, {"username": "hashirama", "password": "testin_pa#@ sswo2rd$"}
        )
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {token_response.data.get('token')}"
        )
        self.test_list = self.client.post(self.list_url, {"name": "Test List"}).data
        self.temp_list_url = f"{self.list_url}{self.test_list.get('list_id')}/"
        self.task_url = f"{self.temp_list_url}tasks/"

    def test_create_task(self):
        task_response = self.client.post(self.task_url, {"title": "new task"})
        self.assertEqual(task_response.status_code, 201)
        task_id = task_response.data.get("task_id")
        task_item: models.Task = models.Task.objects.get(task_id=task_id)
        self.assertEqual(task_item.list.name, "Test List")

    def test_delete_task(self):
        task_response = self.client.post(self.task_url, {"title": "new task"})
        self.assertEqual(task_response.status_code, 201)
        task_id = task_response.data.get("task_id")
        delete_response = self.client.delete(f"{self.task_url}{task_id}/")
        self.assertEqual(delete_response.status_code, 204)

    def test_tasks_for_list(self):
        for i in range(20):
            self.client.post(self.task_url, {"title": f"new task {i+1}"})

        new_list_response = self.client.post(self.list_url, {"name": "New List"})
        new_list = new_list_response.data
        self.assertEqual(new_list_response.status_code, 201)
        new_task_url = f"{self.list_url}{new_list.get('list_id')}/tasks/"
        new_task_response = self.client.post(
            new_task_url, {"title": "Task in new list"}
        )
        self.assertEqual(new_task_response.status_code, 201)
        list_item: models.List = models.List.objects.get(
            list_id=new_list.get("list_id")
        )

        added_task = list_item.tasks.first()

        self.assertEqual(added_task.title, "Task in new list")
