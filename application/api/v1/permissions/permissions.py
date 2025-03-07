from auth.choices.permission_pool import PermissionPool
from rest_framework.permissions import BasePermission

permissions_on_action = {
    "create": PermissionPool.TASK_CREATE.value,
    "read": PermissionPool.TASK_READ.value,
    "update": PermissionPool.TASK_UPDATE.value,
    "destroy": PermissionPool.TASK_DESTROY.value,
}


class IsUserAdmin(BasePermission):
    def has_permission(self, request, view):
        return hasattr(request, "user_data") and request.user_data.role == "admin"


class IsUserAdminOrOwner(BasePermission):
    def has_permission(self, request, view):
        if hasattr(view, "action") and request.user_data.role != "admin":
            return any(
                perm in request.user_data.permissions
                for perm in permissions_on_action.get(view.action)
            )
        return True

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
