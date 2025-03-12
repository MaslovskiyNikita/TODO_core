import uuid

payload_admin = {
    "sub": "1234567890",
    "name": "John Doe",
    "uuid": "3f47f786-8240-46ab-adcf-ee2f54d058d7",
    "role": "admin",
    "permissions": [],
}

payload_user = {
    "sub": "1234567890",
    "name": "John Doe",
    "uuid": "3f47f786-8240-46ab-adcf-ee2f54d058d7",
    "role": "user",
    "permissions": [
        "project_create",
        "task_create",
        "project_read",
        "task_read",
        "project_update",
        "task_update",
        "project_delete",
        "task_delete",
    ],
}

payload_owner = {
    "sub": "1234567890",
    "name": "John Doe",
    "uuid": str(uuid.uuid4()),
    "role": "user",
    "permissions": [
        "project_create",
        "task_create",
        "project_read",
        "task_read",
        "project_update",
        "task_update",
        "project_delete",
        "task_delete",
    ],
}
