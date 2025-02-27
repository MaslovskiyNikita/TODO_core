from rest_framework import serializers

from ..models.project_model import Project


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = [
            "id",
            "description",
            "name",
            "created_at",
            "updated_at",
            "owner",
            "is_archived",
        ]
