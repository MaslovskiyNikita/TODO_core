from auth.choices.permission_pool import PermissionPool
from rest_framework.permissions import BasePermission

permissions_on_action = {
    "create": PermissionPool.PROJECT_CREATE.value,
    "read": PermissionPool.PROJECT_READ.value,
    "update": PermissionPool.PROJECT_UPDATE.value,
    "destroy": PermissionPool.PROJECT_DESTROY.value,
}


class IsAuthenticated(BasePermission):
    def has_permission(self, request, view):
        return hasattr(request, "user_data")


class IsUserAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user_data.role == "admin"  # проверить


class HasTaskPermissions(BasePermission):
    def has_permission(self, request, view):
        if hasattr(view, "action"):
            return any(
                perm in request.user_data.permissions
                for perm in permissions_on_action.get(view.action)
            )
        return True


class IsUserAdminOrOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user_data.role == "admin" or obj.owner == request.user_data.uuid


class IsUserOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user_data.uuid == obj.owner


class IsUserCanUpdate(BasePermission):
    def has_object_permission(self, request, view, obj):
        if hasattr(view, "action"):
            return any(
                perm in request.user_data.permissions
                for perm in permissions_on_action.get(view.action, [])
            )
        return False


class IsUserCanDelete(BasePermission):
    def has_object_permission(self, request, view, obj):
        if hasattr(view, "action"):
            return any(
                perm in request.user_data.permissions
                for perm in permissions_on_action.get(view.action, [])
            )
        return False
