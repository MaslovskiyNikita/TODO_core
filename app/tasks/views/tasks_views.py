from django_filters.rest_framework import DjangoFilterBackend
from permissions.permissions_core import (
    IsUserAdminOrOwner,
    IsUserCanDelete,
    IsUserCanUpdate,
)
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ..filters.filter import TaskFilter
from ..models.task_model import Task
from ..serializers.task_ser import TaskSerializer


class TaskViews(viewsets.ModelViewSet):
    queryset = Task.objects.filter(is_archived=False)
    serializer_class = TaskSerializer
    filterset_class = TaskFilter
    filter_backends = (DjangoFilterBackend,)
    ordering_fields = ["created_at", "title"]
    ordering = ["created_at"]

    permission_class_by_action = {
        "update": [IsAuthenticated | IsUserCanUpdate],
        "partial_update": [IsAuthenticated | IsUserCanUpdate],
        "destroy": [IsUserCanDelete | IsUserAdminOrOwner],
    }

    def get_permissions(self):
        current_action = self.action
        if current_action in ["update", "partial_update"]:
            permissions_classes = self.permission_class_by_action.get(current_action)
        elif current_action in ["destroy"]:
            permissions_classes = self.permission_class_by_action.get(current_action)
        else:
            permissions_classes = []

        return [permissions() for permissions in permissions_classes]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_archived = True
        serializer = self.get_serializer(
            instance, data={"is_archived": instance.is_archived}, partial=True
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, "_prefetched_objects_cache", None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)
