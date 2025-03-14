from auth.choices.permission_pool import PermissionPool
from auth.choices.roles import Role
from rest_framework.permissions import BasePermission

permissions_on_action = {
    "create": PermissionPool.TASK_CREATE.value,
    "read": PermissionPool.TASK_READ.value,
    "update": PermissionPool.TASK_UPDATE.value,
    "destroy": PermissionPool.TASK_DESTROY.value,
}


class HasTasksPermissions(BasePermission):
    def has_permission(self, request, view):
        if hasattr(view, "action"):
            return any(
                perm in request.user_data.permissions
                for perm in permissions_on_action.get(view.action)
            )
        return False
