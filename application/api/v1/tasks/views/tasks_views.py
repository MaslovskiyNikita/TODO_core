from api.v1.filters import TaskFilter
from api.v1.tasks.serializers.task import TaskSerializer
from choices.permission_pool import PermissionPool
from choices.roles import Role
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
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
        "update": PermissionPool.UPDATE.value,
        "partial_update": PermissionPool.PARTIAL_UPDATE.value,
        "destroy": PermissionPool.DESTROY.value,
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
        current_action = self.action
        if current_action in ["update", "partial_update", "destroy"]:
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
