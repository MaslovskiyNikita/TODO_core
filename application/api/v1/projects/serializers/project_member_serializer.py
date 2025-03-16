from projects.models import ProjectMember
from rest_framework import serializers


class ProjectMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectMember
        fields = ("user", "role", "project")
