import pytest
from projects.models import Project
from rest_framework import status

from ...conftest import client_admin, client_owner, client_user


@pytest.mark.django_db
def test_update_project_admin(project: Project, client_admin):
    data = {
        "name": "Updated Test",
        "description": "This is an updated test",
        "owner": project.owner,
    }
    response = client_admin.put(
        f"/api/v1/projects/{project.id}/", data=data, format="json"
    )
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_update_project_user(project: Project, client_user):
    data = {
        "name": "Updated Test",
        "description": "This is an updated test",
        "owner": project.owner,
    }
    response = client_user.put(
        f"/api/v1/projects/{project.id}/", data=data, format="json"
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_update_project_owner(project: Project, client_owner):
    data = {
        "name": "Updated Test",
        "description": "This is an updated test",
        "owner": project.owner,
    }
    response = client_owner.put(
        f"/api/v1/projects/{project.id}/", data=data, format="json"
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_failed_update_project_admin(project: Project, client_admin):
    data: dict = {}
    response = client_admin.put(
        f"/api/v1/projects/{project.id}/", data=data, format="json"
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_failed_update_project_user(project: Project, client_user):
    data: dict = {}
    response = client_user.put(
        f"/api/v1/projects/{project.id}/", data=data, format="json"
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_failed_update_project_owner(project: Project, client_owner):
    data: dict = {}
    response = client_owner.put(
        f"/api/v1/projects/{project.id}/", data=data, format="json"
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
