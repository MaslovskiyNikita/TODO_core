from enum import Enum

from api.v1.projects import permissions
from rest_framework.permissions import IsAuthenticated


class PermissionPool(Enum):
    CREATE = [IsAuthenticated]
    READ = [permissions.IsUserAdminOrOwner]
    UPDATE = [IsAuthenticated | permissions.IsUserCanUpdate]
    PARTIAL_UPDATE = [IsAuthenticated | permissions.IsUserCanUpdate]
    DESTROY = [permissions.IsUserCanDelete | permissions.IsUserAdminOrOwner]
