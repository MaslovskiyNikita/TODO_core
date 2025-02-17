import uuid

from django.db import models
from tasks.models.task_model import Task


class Subscriber(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.UUIDField()
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="subscribers")

    def __str__(self):
        return f"{self.user.username} subscribed to {self.task.title}"
