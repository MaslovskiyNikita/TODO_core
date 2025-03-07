from enum import Enum


class PermissionPool(Enum):
    TASK_CREATE = ["task_create"]
    TASK_READ = ["task_read"]
    TASK_UPDATE = ["task_update"]
    TASK_PARTIAL_UPDATE = ["task_partial_update"]
    TASK_DESTROY = ["task_destroy"]

    PROJECT_CREATE = ["project_create"]
    PROJECT_READ = ["project_read"]
    PROJECT_UPDATE = ["project_update"]
    PROJECT_PARTIAL_UPDATE = ["project_partial_update"]
    PROJECT_DESTROY = ["project_destroy"]
