import uuid

from django.db import models


class Project(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.UUIDField()
    is_archived = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class ProjectMember(models.Model):

    ROLES = (("redactor", "redactor"), ("viewer", "viewer"))

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="members"
    )
    user = models.UUIDField()
    role = models.CharField(max_length=9, choices=ROLES)

    def __str__(self):
        return f"{self.user} - {self.project.name}"
