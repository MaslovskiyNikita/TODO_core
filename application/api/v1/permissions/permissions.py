from auth.choices.roles import Role
from projects.models.project_model import ProjectMember
from rest_framework.permissions import BasePermission


class IsAuthenticated(BasePermission):
    def has_permission(self, request, view):
        return hasattr(request, "user_data")


class IsUserAdmin(BasePermission):
    def has_permission(self, request, view):
        return (
            hasattr(request, "user_data") and request.user_data.role == Role.ADMIN.value
        )


class IsUserOwner(BasePermission):
    def has_permission(self, request, view):
        return hasattr(request, "user_data")

    def has_object_permission(self, request, view, obj):
        return str(request.user_data.uuid) == str(obj.owner)


class IsUserRedactor(BasePermission):
    def has_permission(self, request, view):
        return hasattr(request, "user_data")

    def has_object_permission(self, request, view, obj):
        project_member = ProjectMember.objects.get(
            project=obj.id, user=request.user_data.uuid
        )
        if project_member != None and project_member.role == "redactor":
            return True
        return False
