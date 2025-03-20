from api.v1.permissions.permissions import IsUserAdmin, IsUserOwner
from api.v1.projects.permissions import (
    AddProjectMember,
    DeleteProjectMember,
    HasProjectsPermissions,
    PatchProjectMember,
    PutProjectMember,
)
from api.v1.projects.serializers.project_member_serializer import (
    ProjectMemberSerializer,
)
from api.v1.projects.serializers.project_serializer import ProjectSerializer
from auth.choices.roles import Role
from django.db.models import Q
from projects.models import Project, ProjectMember
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from rest_framework.response import Response


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.filter(is_archived=False)
    serializer_class = ProjectSerializer

    permission_class_by_action = {
        "update": [IsUserOwner | HasProjectsPermissions | IsUserAdmin],
        "partial_update": [HasProjectsPermissions | IsUserAdmin | IsUserOwner],
        "destroy": [HasProjectsPermissions | IsUserAdmin | IsUserOwner],
        "add_member": [IsUserOwner | IsUserAdmin | AddProjectMember],
        "put_member": [IsUserOwner | IsUserAdmin | PutProjectMember],
        "patch_member": [IsUserOwner | IsUserAdmin | PatchProjectMember],
        "delete_member": [IsUserOwner | IsUserAdmin | DeleteProjectMember],
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

    @action(methods="get", detail=False, url_path="list_members")
    def list_members(self, request):
        return ProjectMember.objects.all()

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

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @members_detail.mapping.delete
    def delete_member(self, request, pk=None, user_pk=None):

        project = self.get_object()

        if not ProjectMember.objects.filter(project=project, user=user_pk).exists():
            return Response(status=status.HTTP_404_NOT_FOUND)

        member = ProjectMember.objects.get(project=project, user=user_pk)
        member.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @members_detail.mapping.put
    def update_member(self, request, pk=None, user_pk=None):
        project = self.get_object()

        try:
            member = ProjectMember.objects.get(project=project, user=user_pk)
        except ProjectMember.DoesNotExist:
            raise NotFound("Member not found")

        serializer = ProjectMemberSerializer(
            instance=member, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    @members.mapping.patch
    def member_patch(self, request, pk=None):
        project = self.get_object()

        try:
            member = ProjectMember.objects.get(project=project, user=user_pk)
        except ProjectMember.DoesNotExist:
            raise NotFound("Member not found")

        serializer = ProjectMemberSerializer(
            instance=member, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

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
