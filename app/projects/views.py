from rest_framework import status, viewsets
from rest_framework.response import Response

from .models.project_model import Project
from .permissions import IsUserAdmin, IsUserAdminOrOwner
from .serializer import ProjectSerializer


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def get_permissions(self):

        current_action = self.action

        if current_action in ["create", "update", "destroy", "partial_update"]:
            permission_classes = [IsUserAdminOrOwner]
        else:
            permission_classes = []

        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data["owner"] = request.data_user.uuid
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        project = self.get_object()
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        project = self.get_object()
        return super().destroy(request, *args, **kwargs)
