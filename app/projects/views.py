from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models.project_model import Project
from .serializer import ProjectSerializer


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    @action(detail=False, methods=["delete"])
    def delete_all(self, request):

        count, _ = Project.objects.all().delete()
        return Response(
            {"detail": f"{count} projects deleted."}, status=status.HTTP_204_NO_CONTENT
        )

    @action(detail=True, methods=["get"])
    def project_id(self, request, pk=None):

        try:
            project = self.get_object()
            serializer = self.get_serializer(project)
            return Response(serializer.data)
        except Project.DoesNotExist:
            return Response(
                {"detail": "Project not found."}, status=status.HTTP_404_NOT_FOUND
            )
