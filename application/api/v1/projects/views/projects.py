from api.v1.projects.serializers.project_serializer import ProjectSerializer
from choices.permission_pool import PermissionPool
from choices.roles import Role
from django.db.models import Q
from projects.models import Project, ProjectMember
from rest_framework import status, viewsets
from rest_framework.response import Response


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.filter(is_archived=False)
    serializer_class = ProjectSerializer
    permission_class_by_action = {
        "update": PermissionPool.UPDATE.value,
        "partial_update": PermissionPool.PARTIAL_UPDATE.value,
        "destroy": PermissionPool.DESTROY.value,
    }

    def get_queryset(self):
        if self.request.user_data.role == Role.ADMIN.value:
            return Project.objects.filter(is_archived=False)
        else:
            return Project.objects.filter(
                Q(members__user=self.request.user_data.uuid)
                | Q(owner=self.request.user_data.uuid)
            )

    def get_permissions(self):
        current_action = self.action
        if current_action in ["update", "partial_update", "destroy"]:
            permissions_classes = self.permission_class_by_action.get(current_action)
        else:
            permissions_classes = []

        return [permissions() for permissions in permissions_classes]

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data["owner"] = request.user_data.uuid
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

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
