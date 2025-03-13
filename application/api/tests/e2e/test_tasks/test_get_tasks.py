import pytest
from api.tests.conftest import client_admin, client_owner, client_user
from rest_framework import status
from tasks.models import Task


@pytest.mark.django_db
def test_get_tasks_admin(task: Task, client_admin):
    response = client_admin.get("/api/v1/tasks/")
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json().get("results"), list)


@pytest.mark.django_db
def test_get_tasks_user(task: Task, client_user):
    response = client_user.get("/api/v1/tasks/")
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json().get("results"), list)


@pytest.mark.django_db
def test_get_tasks_owner(task: Task, client_owner):
    response = client_owner.get("/api/v1/tasks/")
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json().get("results"), list)


@pytest.mark.django_db
def test_get_task_by_id_admin(task: Task, client_admin):
    response = client_admin.get(f"/api/v1/tasks/{task.id}/")
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_get_task_by_id_user(task: Task, client_user):
    response = client_user.get(f"/api/v1/tasks/{task.id}/")
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_get_task_by_id_owner(task: Task, client_owner):
    response = client_owner.get(f"/api/v1/tasks/{task.id}/")
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_failed_get_task_by_id_admin(task: Task, client_admin):
    response = client_admin.get(f"/api/v1/tasks/aaa/")
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_failed_get_task_by_id_user(task: Task, client_user):
    response = client_user.get(f"/api/v1/tasks/aaa/")
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_failed_get_task_by_id_owner(task: Task, client_owner):
    response = client_owner.get(f"/api/v1/tasks/aaa/")
    assert response.status_code == status.HTTP_404_NOT_FOUND
