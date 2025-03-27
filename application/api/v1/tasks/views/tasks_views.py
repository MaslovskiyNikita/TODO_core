from api.v1.filters.filters import TaskFilter
from api.v1.permissions.permissions import IsUserAdmin, IsUserOwner
from api.v1.tasks.permissions import HasTasksPermissions
from api.v1.tasks.serializers.subscriber import TaskSubscriberSerializer
from api.v1.tasks.serializers.task import TaskSerializer
from auth.choices.roles import Role
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from tasks.models.task_model import Task, TaskSubscriber


class TaskViews(viewsets.ModelViewSet):
    queryset = Task.objects.filter(is_archived=False)
    serializer_class = TaskSerializer
    filterset_class = TaskFilter
    filter_backends = (DjangoFilterBackend,)
    ordering_fields = ["created_at", "title"]
    ordering = ["created_at"]

    permission_class_by_action = {
        "update": [IsUserOwner | HasTasksPermissions | IsUserAdmin],
        "partial_update": [
            IsUserOwner | IsAuthenticated | HasTasksPermissions | IsUserAdmin
        ],
        "perform_destroy": [HasTasksPermissions | IsUserAdmin | IsUserOwner],
    }

    def get_queryset(self):
        if self.request.user_data.role == Role.ADMIN.value:
            return Task.objects.filter(is_archived=False)
        else:
            return Task.objects.filter(
                Q(subscribers__user=self.request.user_data.uuid)
                | Q(project__owner=self.request.user_data.uuid)
                | Q(assigned_to=self.request.user_data.uuid)
                | Q(owner=self.request.user_data.uuid)
            )

    @action(detail=True, methods=["post"], url_path="subscribers")
    def subscribe_on_task(self, request, pk=None):

        task = self.get_object()

        data = request.data.copy()
        data["task"] = task.id

        if TaskSubscriber.objects.filter(user=request.user_data.uuid).exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)

        serializer = TaskSubscriberSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_permissions(self):
        permissions_classes = self.permission_class_by_action.get(self.action, [])

        return [permission() for permission in permissions_classes]

    def perform_destroy(self, instance):
        instance.is_archived = True
        instance.save()
