from enum import Enum


class PermissionPool(Enum):
    TASK_CREATE = ["task_create"]
    TASK_READ = ["task_read"]
    TASK_UPDATE = ["task_update"]
    TASK_PARTIAL_UPDATE = ["task_partial_update"]
    TASK_DESTROY = ["task_destroy"]
    TASK_ADD_MEMBER = ["task_add_member"]
    TASK_UPDATE_MEMBER = ["task_update_member"]
    TASK_DELETE_MEMBER = ["task_delete_member"]

    PROJECT_CREATE = ["project_create"]
    PROJECT_READ = ["project_read"]
    PROJECT_UPDATE = ["project_update"]
    PROJECT_PARTIAL_UPDATE = ["project_partial_update"]
    PROJECT_DESTROY = ["project_destroy"]
    PROJECT_ADD_MEMBER = ["project_add_member"]
    PROJECT_UPDATE_MEMBER = ["project_update_member"]
    PROJECT_DELETE_MEMBER = ["project_delete_member"]
