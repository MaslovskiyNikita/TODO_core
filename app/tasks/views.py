from django_filters.rest_framework import DjangoFilterBackend
from permissions.IsUserAdminOrOwner import (
    IsUserAdminOrOwner,
    IsUserCanDelete,
    IsUserCanUpdate,
)
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .filter import TaskFilter
from .models.task_model import Task
from .serializer import TaskSerializer


class TaskListCreate(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    filterset_fields = ["project", "assigned_to", "status"]
    ordering_fields = ["created_at", "title"]
    ordering = ["created_at"]

    def get_permissions(self):
        current_action = self.action

        if current_action in ["update", "partial_update"]:
            permission_classes = [IsUserAdminOrOwner | IsUserCanUpdate]
        elif current_action in ["destroy"]:
            permission_classes = [IsUserCanDelete | IsUserAdminOrOwner]
        else:
            permission_classes = []

        return [permission() for permission in permission_classes]
