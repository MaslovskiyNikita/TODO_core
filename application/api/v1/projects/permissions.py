from auth.choices.permission_pool import PermissionPool
from auth.choices.roles import Role
from rest_framework.permissions import BasePermission

permissions_on_action = {
    "create": PermissionPool.PROJECT_CREATE.value,
    "read": PermissionPool.PROJECT_READ.value,
    "update": PermissionPool.PROJECT_UPDATE.value,
    "update_partial": PermissionPool.PROJECT_UPDATE.value,
    "destroy": PermissionPool.PROJECT_DESTROY.value,
    "add_member": PermissionPool.PROJECT_ADD_MEMBER.value,
    "put_member": PermissionPool.PROJECT_UPDATE_MEMBER.value,
    "patch_member": PermissionPool.PROJECT_UPDATE_MEMBER.value,
    "delete_member": PermissionPool.PROJECT_DELETE_MEMBER.value,
}


class HasProjectsPermissions(BasePermission):
    def has_permission(self, request, view):
        if hasattr(view, "action"):
            return any(
                perm in request.user_data.permissions
                for perm in permissions_on_action.get(view.action, [])
            )
        return False
