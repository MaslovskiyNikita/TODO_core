from api.v1.projects.permissions import (
    IsAuthenticated,
    IsUserAdmin,
    IsUserAdminOrOwner,
    IsUserCanDelete,
    IsUserCanUpdate,
    IsUserOwner,
)
from api.v1.projects.serializers.project_serializer import ProjectSerializer
from auth.choices.roles import Role
from django.db.models import Q
from projects.models import Project, ProjectMember
from rest_framework import status, viewsets
from rest_framework.response import Response


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.filter(is_archived=False)
    serializer_class = ProjectSerializer

    permission_class_by_action = {
        "update": [IsUserOwner | IsUserCanUpdate | IsUserAdmin],
        "partial_update": [IsUserCanUpdate | IsUserAdminOrOwner],
        "destroy": [IsUserCanDelete | IsUserAdminOrOwner],
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
        permissions_classes = self.permission_class_by_action.get(self.action, [])

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
            instance._prefetched_objects_cache = {}

        return Response(serializer.data, status=204)
