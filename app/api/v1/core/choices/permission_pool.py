from enum import Enum

from projects import permissions
from rest_framework.permissions import IsAuthenticated


class PermissionPool(Enum):
    UPDATE = [IsAuthenticated | permissions.IsUserCanUpdate]
    PARTIAL_UPDATE = ([IsAuthenticated | permissions.IsUserCanUpdate],)
    DESTROY = ([permissions.IsUserCanDelete | permissions.IsUserAdminOrOwner],)
