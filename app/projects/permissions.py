from rest_framework.permissions import BasePermission


class IsUserAdmin(BasePermission):

    def has_permission(self, request, view):

        if request.method in ["GET", "HEAD", "OPTIONS"]:
            return True
        print(request.data_user)
        return True if request.data_user["is_staff"] == True else False
