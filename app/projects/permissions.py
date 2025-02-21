from rest_framework.permissions import BasePermission


class IsUserAdmin(BasePermission):
    def has_permission(self, request, view):
        if hasattr(request, "data_user") and request.data_user.role == "admin":
            return True
        return False


class IsUserAdminOrOwner(BasePermission):
    def has_permission(self, request, view):
        if request.method in ["GET", "HEAD", "OPTIONS"]:
            return True

        if hasattr(request, "data_user"):
            return request.data_user.role == "admin"

        return False

    def has_object_permission(self, request, view, obj):
        if hasattr(request, "data_user"):
            return (
                request.data_user.role == "admin" or obj.owner == request.data_user.uuid
            )

        return False
