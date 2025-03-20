from projects.models import ProjectMember
from rest_framework import serializers


class ProjectMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectMember
        fields = ("user", "role", "project")

    def get_fields(self):
        fields = super().get_fields()
        if self.instance is not None:
            fields["user"].read_only = True
        return fields
