from api.v1.permissions.permissions import (
    IsAuthenticated,
    IsUserAdmin,
    IsUserOwner,
    IsUserRedactor,
)
from api.v1.projects.permissions import HasProjectsPermissions
from api.v1.projects.serializers.project_member_serializer import (
    ProjectMemberSerializer,
)
from api.v1.projects.serializers.project_serializer import ProjectSerializer
from auth.choices.roles import Role
from django.db.models import Q
from django.shortcuts import get_object_or_404
from projects.celery_tasks.tasks import send_project_invitation_email
from projects.models import Project, ProjectMember
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.filter(is_archived=False)
    serializer_class = ProjectSerializer

    permission_class_by_action = {
        "list": [IsAuthenticated],
        "create": [IsAuthenticated],
        "update": [IsUserOwner | HasProjectsPermissions | IsUserAdmin | IsUserRedactor],
        "partial_update": [
            HasProjectsPermissions | IsUserAdmin | IsUserOwner | IsUserRedactor
        ],
        "destroy": [HasProjectsPermissions | IsUserAdmin | IsUserOwner],
        "add_member": [IsUserOwner | IsUserAdmin | HasProjectsPermissions],
        "put_member": [IsUserOwner | IsUserAdmin | HasProjectsPermissions],
        "patch_member": [IsUserOwner | IsUserAdmin | HasProjectsPermissions],
        "delete_member": [IsUserOwner | IsUserAdmin | HasProjectsPermissions],
    }

    def get_queryset(self):
        if self.request.user_data.role == Role.ADMIN.value:
            return Project.objects.filter(is_archived=False)
        else:
            return Project.objects.filter(
                (
                    Q(members__user=self.request.user_data.uuid)
                    | Q(owner=self.request.user_data.uuid)
                )
                & Q(is_archived=False)
            )

    def get_permissions(self):
        permissions_classes = self.permission_class_by_action.get(self.action, [])
        return [permissions() for permissions in permissions_classes]

    @action(methods=["get"], detail=True, url_path="members_list")
    def list_members(self, request, pk=None):
        project = self.get_object()
        data = ProjectMember.objects.filter(project=project)
        serializer = ProjectMemberSerializer(data, many=True)
        return Response(serializer.data)

    @action(methods=[], detail=True, url_path="members")
    def members(self, request, pk):
        pass

    @action(methods=[], detail=True, url_path="members/(?P<user_pk>[^/.]+)")
    def members_detail(self, request, user_pk):
        pass

    @members.mapping.post
    def add_member(self, request, pk=None):
        project = self.get_object()
        data = request.data.copy()
        data["project"] = project.id
        user_uuid = data.get("user")

        if ProjectMember.objects.filter(project=project, user=user_uuid).exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)

        serializer = ProjectMemberSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        send_project_invitation_email.delay(
            str(user_uuid), str(project.name), str(project.owner)
        )

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @members_detail.mapping.delete
    def delete_member(self, request, pk=None, user_pk=None):
        project = self.get_object()
        member = get_object_or_404(ProjectMember, project=project, user=user_pk)
        member.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def _update_member(self, request, pk, user_pk, partial):
        project = self.get_object()
        member = get_object_or_404(ProjectMember, project=project, user=user_pk)
        serializer = ProjectMemberSerializer(
            instance=member, data=request.data, partial=partial
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @members_detail.mapping.put
    def update_member(self, request, pk=None, user_pk=None):
        return self._update_member(request, pk, user_pk, partial=False)

    @members_detail.mapping.patch
    def member_patch(self, request, pk=None, user_pk=None):
        return self._update_member(request, pk, user_pk, partial=True)

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
