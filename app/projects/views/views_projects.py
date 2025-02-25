from permissions.permissions_core import (
    IsUserAdminOrOwner,
    IsUserCanDelete,
    IsUserCanUpdate,
)
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ..models.project_model import Project
from ..serializators.serializer import ProjectSerializer


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def get_permissions(self):
        current_action = self.action

        if current_action in ["update", "partial_update"]:
            permission_classes = [IsUserAdminOrOwner | IsUserCanUpdate]
        elif current_action in ["destroy"]:
            permission_classes = [IsUserCanDelete | IsUserAdminOrOwner]
        else:
            # permission_classes = [IsAuthenticated]
            permission_classes = []

        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data["owner"] = request.user_data.uuid
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
