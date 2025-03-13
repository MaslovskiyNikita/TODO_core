from auth.choices.permission_pool import PermissionPool
from auth.choices.roles import Role
from rest_framework.permissions import BasePermission


class IsAuthenticated(BasePermission):
    def has_permission(self, request, view):
        return hasattr(request, "user_data")


class IsUserAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user_data.role == Role.ADMIN.value


class IsUserOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user_data.uuid == obj.owner


class IsUserAdminOrOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return IsUserAdmin | IsUserOwner
