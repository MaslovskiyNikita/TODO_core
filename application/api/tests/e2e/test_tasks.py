import datetime
import uuid

import pytest
from projects.models import Project
from rest_framework import status
from tasks.models import Task

from ..conftest import client, task


@pytest.mark.django_db
def test_get_tasks(task: Task, client):
    response = client.get("/api/v1/tasks/")
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json().get("results"), list)


@pytest.mark.django_db
def test_get_task_by_id(task: Task, client):
    response = client.get(f"/api/v1/tasks/{task.id}/")
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_failed_get_task_by_id(task: Task, client):
    response = client.get(f"/api/v1/tasks/aaa/")
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_create_task(task: Task, project: Project, client):
    data = {
        "title": "Task test",
        "description": "Task description",
        "status": "asdasd",
        "due_date": datetime.datetime.now().isoformat(),
        "project": project.id,
        "assigned_to": str(uuid.uuid4()),
    }
    response = client.post("/api/v1/tasks/", data=data)
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
def test_failed_create_task(task: Task, project: Project, client):
    data: dict = {}
    response = client.post("/api/v1/tasks/", data=data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_update_task(task: Task, project: Project, client):

    data = {
        "title": "Task test",
        "description": "Task description",
        "status": "prikol",
        "due_date": datetime.datetime.now().isoformat(),
        "project": project.id,
        "assigned_to": str(uuid.uuid4()),
    }
    response = client.put(f"/api/v1/tasks/{task.id}/", data=data)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_failed_update_task(task: Task, project: Project, client):

    data: dict = {}
    response = client.put(f"/api/v1/tasks/aaa/", data=data)
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_delete_task(task, client):
    response = client.delete(f"/api/v1/tasks/{task.id}/")
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_failed_delete_task(task, client):
    response = client.delete(f"/api/v1/tasks/aaa/")
    assert response.status_code == status.HTTP_404_NOT_FOUND
