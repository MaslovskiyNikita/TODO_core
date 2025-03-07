import datetime
import uuid

import pytest
from conftest import client, task

from application.projects.models import Project
from application.tasks.models import Task


@pytest.mark.django_db
def test_get_tasks(task: Task, client):
    response = client.get("/api/v1/tasks/")
    assert response.status_code == 200
    assert isinstance(response.json().get("results"), list)


@pytest.mark.django_db
def test_get_task_by_id(task: Task, client):
    response = client.get(f"/api/v1/tasks/{task.id}/")
    assert response.status_code == 200


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
    assert response.status_code == 201


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
    assert response.status_code == 200


@pytest.mark.django_db
def test_delete_task(task, client):
    response = client.delete(f"/api/v1/tasks/{task.id}/")
    assert response.status_code == 200
