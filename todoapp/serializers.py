from rest_framework import serializers
from todoapp import models


class ListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.List
        fields = ("list_id", "name", "created_on", "last_modified")
        extra_kwargs = {
            "list_id": {"read_only": True},
            "created_on": {"read_only": True},
            "last_modified": {"read_only": True},
        }


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Task
        fields = (
            "task_id",
            "title",
            "description",
            "completed",
            "due_date",
            "last_modified",
            "created_on",
        )
        extra_kwargs = {
            "task_id": {"read_only": True},
            "created_on": {"read_only": True},
            "last_modified": {"read_only": True},
        }
