from rest_framework.permissions import BasePermission

permission_on_action = {
    "create": ["project_create", "task_create"],
    "read": ["project_read", "task_read"],
    "update": ["project_update", "task_update"],
    "destroy": ["project_delete", "task_delete"],
}


class IsUserAdmin(BasePermission):
    def has_permission(self, request, view):
        return hasattr(request, "user_data") and request.user_data.role == "admin"


class IsUserAdminOrOwner(BasePermission):
    def has_permission(self, request, view):
        if hasattr(view, "action"):
            return any(
                perm in request.user_data.permission
                for perm in permission_on_action.get(view.action, [])
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
                perm in request.user_data.permission
                for perm in permission_on_action.get(view.action, [])
            )
        return False


class IsUserCanDelete(BasePermission):
    def has_object_permission(self, request, view, obj):
        if hasattr(view, "action"):
            return any(
                perm in request.user_data.permission
                for perm in permission_on_action.get(view.action, [])
            )
        return False
