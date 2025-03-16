from api.v1.permissions.permissions import IsUserAdmin, IsUserOwner
from api.v1.projects.permissions import HasProjectsPermissions
from api.v1.projects.serializers.project_member_serializer import (
    ProjectMemberSerializer,
)
from api.v1.projects.serializers.project_serializer import ProjectSerializer
from auth.choices.roles import Role
from django.db.models import Q
from projects.models import Project, ProjectMember
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.filter(is_archived=False)
    serializer_class = ProjectSerializer

    permission_class_by_action = {
        "update": [IsUserOwner | HasProjectsPermissions | IsUserAdmin],
        "partial_update": [HasProjectsPermissions | IsUserAdmin | IsUserOwner],
        "destroy": [HasProjectsPermissions | IsUserAdmin | IsUserOwner],
        "add_user_to_project": [IsUserOwner | IsUserAdmin],
    }

    def get_queryset(self):
        if self.request.user_data.role == Role.ADMIN.value:
            return Project.objects.filter(is_archived=False)
        else:
            return Project.objects.filter(
                Q(members__user=self.request.user_data.uuid)
                | Q(owner=self.request.user_data.uuid)
            )

    @action(detail=True, methods=["post"])
    def add_user_to_project(self, request, pk=None):

        project = self.get_object()

        if not (
            project.owner == request.user_data.uuid
            or request.user_data.role == Role.ADMIN.value
        ):
            "Проверка на права добавления пользователя"
            return status.HTTP_403_FORBIDDEN

        data = request.data.copy()
        data["project"] = project.id
        user_uuid = data.get("user")

        if ProjectMember.objects.filter(project=project, user=user_uuid).exists():
            "Проверка на то что есть ли пользователь уже в проекте"
            return status.HTTP_409_CONFLICT

        print(data)
        serializer = ProjectMemberSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

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

    def perform_destroy(self, instance):
        instance.is_archived = True
        instance.save()
