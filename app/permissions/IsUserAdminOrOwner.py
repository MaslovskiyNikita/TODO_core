from rest_framework.permissions import BasePermission

permission_on_action = {
    "create": ["project_create", "task_create"],
    "read": ["project_read", "task_read"],
    "update": ["project_update", "task_update"],
    "desrtoy": ["project_delete", "task_delete"],
}


class IsUserAdmin(BasePermission):
    def has_permission(self, request, view):
        if hasattr(request, "data_user") and request.data_user.role == "admin":
            return True
        return False


class IsUserAdminOrOwner(BasePermission):
    def has_permission(self, request, view):

        if permission_on_action[view.action] in request.data_user.permissions:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        return request.data_user.role == "admin" or obj.owner == request.data_user.uuid


class IsUserOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return True if request.data_suer.uuid == obj.owner else False


class IsUserCanUpdate(BasePermission):
    def has_object_permission(self, request, view, obj):
        return permission_on_action[view.action] in request.user_data.permissions


class IsUserCanDelete(BasePermission):
    def has_object_permission(self, request, view, obj):
        return permission_on_action[view.action] in request.user_data.permissions
