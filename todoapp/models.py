from django.db import models
from django.conf import settings
import uuid

# Create your models here.


class List(models.Model):
    """
    Database model for task lists.
    """

    list_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(blank=False, max_length=30)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="task_lists"
    )
    created_on = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "task_lists"
        get_latest_by = ["-priority", "created_on"]


class Task(models.Model):
    """
    Database model for tasks.
    """

    task_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(null=False, blank=False, max_length=220)
    description = models.TextField(blank=True, max_length=2500)
    completed = models.BooleanField(default=False)
    due_date = models.DateTimeField(blank=True, null=True, default=None)
    last_modified = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)
    list = models.ForeignKey(List, on_delete=models.CASCADE, related_name="tasks")

    class Meta:
        db_table = "task_items"
        get_latest_by = ["-priority", "created_on"]
