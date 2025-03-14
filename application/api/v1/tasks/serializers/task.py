from rest_framework import serializers
from tasks.models.task_model import Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            "id",
            "title",
            "description",
            "status",
            "due_date",
            "created_at",
            "updated_at",
            "project",
            "owner",
            "assigned_to",
        ]
