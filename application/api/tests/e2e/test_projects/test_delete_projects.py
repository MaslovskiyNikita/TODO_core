import pytest
from projects.models import Project
from rest_framework import status

from ...conftest import client_admin, client_owner, client_user


@pytest.mark.django_db
def test_delete_project_admin(project, client_admin):
    response = client_admin.delete(f"/api/v1/projects/{project.id}/")
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_delete_project_user(project, client_user):
    response = client_user.delete(f"/api/v1/projects/{project.id}/")
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_delete_project_owner(project, client_owner):
    response = client_owner.delete(f"/api/v1/projects/{project.id}/")
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_failed_delete_project_admin(project, client_admin):
    response = client_admin.delete(f"/api/v1/projects/aaa/")
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_failed_delete_project_user(project, client_user):
    response = client_user.delete(f"/api/v1/projects/aaa/")
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_failed_delete_project_owner(project, client_owner):
    response = client_owner.delete(f"/api/v1/projects/aaa/")
    assert response.status_code == status.HTTP_404_NOT_FOUND
