from rest_framework import status, viewsets
from rest_framework.response import Response

from .models.project_model import Project
from .permissions import IsUserAdmin
from .serializer import ProjectSerializer


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsUserAdmin]

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        if request.user.is_authenticated:
            data["owner"] = request.user.id
        else:
            data["owner"] = None
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        project = self.get_object()
        if project.owner != request.user.id and not request.user.is_staff:
            raise PermissionDenied("You do not have permission to edit this project.")
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        project = self.get_object()
        if project.owner != request.user.id and not request.user.is_staff:
            raise PermissionDenied("You do not have permission to delete this project.")
        return super().destroy(request, *args, **kwargs)
