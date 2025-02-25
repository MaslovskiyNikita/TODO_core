from rest_framework import serializers

from ..models.project_model import Project


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ["id", "name", "created_at", "updated_at", "owner"]
