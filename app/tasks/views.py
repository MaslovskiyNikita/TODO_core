from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models.task_model import Task
from .serializer import TaskSerializer


class TaskListCreate(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    @action(detail=False, methods=["delete"])
    def delete_all(self, request):
        count, _ = Task.objects.all().delete()
        return Response(
            {"detail": f"{count} tasks deleted."}, status=status.HTTP_204_NO_CONTENT
        )

    @action(detail=True, methods=["get"])
    def task_id(self, request, pk=None):
        try:
            task = self.get_object()
            serializer = self.get_serializer(task)
            return Response(serializer.data)
        except Task.DoesNotExist:
            return Response(
                {"detail": "Task not found."}, status=status.HTTP_404_NOT_FOUND
            )
