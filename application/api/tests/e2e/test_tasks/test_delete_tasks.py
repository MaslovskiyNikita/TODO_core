import pytest
from api.tests.conftest import client_admin, client_owner, client_user
from rest_framework import status
from tasks.models import Task


@pytest.mark.django_db
def test_delete_task_admin(task, client_admin):
    response = client_admin.delete(f"/api/v1/tasks/{task.id}/")
    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db
def test_delete_task_user(task, client_user):
    response = client_user.delete(f"/api/v1/tasks/{task.id}/")
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_delete_task_owner(task, client_owner):
    response = client_owner.delete(f"/api/v1/tasks/{task.id}/")
    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db
def test_failed_delete_task_admin(task, client_admin):
    response = client_admin.delete(f"/api/v1/tasks/aaa/")
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_failed_delete_task_user(task, client_user):
    response = client_user.delete(f"/api/v1/tasks/aaa/")
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_failed_delete_task_owner(task, client_owner):
    response = client_owner.delete(f"/api/v1/tasks/aaa/")
    assert response.status_code == status.HTTP_404_NOT_FOUND
