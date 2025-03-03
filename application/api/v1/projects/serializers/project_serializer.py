from projects.models import Project
from rest_framework import serializers


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
