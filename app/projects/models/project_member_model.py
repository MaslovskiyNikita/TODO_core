import uuid

from django.db import models

from .project_model import Project


class ProjectMember(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="members"
    )
    user = models.UUIDField()
    role = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.user.username} in {self.project.name}"
