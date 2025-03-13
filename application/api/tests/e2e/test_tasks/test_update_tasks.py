import datetime
import uuid

import pytest
from api.tests.conftest import client_admin, client_owner, client_user
from projects.models import Project
from rest_framework import status
from tasks.models import Task


@pytest.mark.django_db
def test_update_task_admin(task: Task, project: Project, client_admin):
    data = {
        "title": "Task test",
        "description": "Task description",
        "status": "prikol",
        "due_date": datetime.datetime.now().isoformat(),
        "project": project.id,
        "owner": str(uuid.uuid4()),
        "assigned_to": str(uuid.uuid4()),
    }
    response = client_admin.put(f"/api/v1/tasks/{task.id}/", data=data)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_update_task_user(task: Task, project: Project, client_user):
    data = {
        "title": "Task test",
        "description": "Task description",
        "status": "prikol",
        "due_date": datetime.datetime.now().isoformat(),
        "project": project.id,
        "assigned_to": str(uuid.uuid4()),
    }
    response = client_user.put(f"/api/v1/tasks/{task.id}/", data=data)
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_update_task_owner(task: Task, project: Project, client_owner):
    data = {
        "title": "Task test",
        "description": "Task description",
        "status": "prikol",
        "due_date": datetime.datetime.now().isoformat(),
        "project": project.id,
        "owner": str(uuid.uuid4()),
        "assigned_to": str(uuid.uuid4()),
    }
    response = client_owner.put(f"/api/v1/tasks/{task.id}/", data=data)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_failed_update_task_admin(task: Task, project: Project, client_admin):
    data: dict = {}
    response = client_admin.put(f"/api/v1/tasks/aaa/", data=data)
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_failed_update_task_user(task: Task, project: Project, client_user):
    data: dict = {}
    response = client_user.put(f"/api/v1/tasks/aaa/", data=data)
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_failed_update_task_owner(task: Task, project: Project, client_owner):
    data: dict = {}
    response = client_owner.put(f"/api/v1/tasks/aaa/", data=data)
    assert response.status_code == status.HTTP_404_NOT_FOUND
