import uuid

from django.db import models
from projects.models.project_model import Project


class Task(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=50)
    due_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="tasks")
    owner = models.UUIDField()
    assigned_to = models.UUIDField()
    is_archived = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class TaskSubscriber(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.UUIDField()
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="subscribers")

    def __str__(self):
        return f"{self.user.username} subscribed to {self.task.title}"
