from api.v1.filters.filters import TaskFilter
from api.v1.tasks.permissions import (
    IsAuthenticated,
    IsUserAdmin,
    IsUserAdminOrOwner,
    IsUserCanDelete,
    IsUserCanUpdate,
    IsUserOwner,
)
from api.v1.tasks.serializers.task import TaskSerializer
from auth.choices.permission_pool import PermissionPool
from auth.choices.roles import Role
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from tasks.models.task_model import Task


class TaskViews(viewsets.ModelViewSet):
    queryset = Task.objects.filter(is_archived=False)
    serializer_class = TaskSerializer
    filterset_class = TaskFilter
    filter_backends = (DjangoFilterBackend,)
    ordering_fields = ["created_at", "title"]
    ordering = ["created_at"]

    permission_class_by_action = {
        "update": [IsUserCanUpdate | IsUserAdminOrOwner],
        "partial_update": [IsAuthenticated | IsUserCanUpdate],
        "destroy": [IsUserCanDelete | IsUserAdminOrOwner],
    }

    def get_queryset(self):
        if self.request.user_data.role == Role.ADMIN.value:
            return Task.objects.filter(is_archived=False)
        else:
            return Task.objects.filter(
                Q(subscribers__user=self.request.user_data.uuid)
                | Q(project__owner=self.request.user_data.uuid)
            )

    def get_permissions(self):
        permissions_classes = self.permission_class_by_action.get(self.action, [])

        return [permission() for permission in permissions_classes]

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
