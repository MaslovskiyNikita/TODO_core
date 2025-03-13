import pytest
from api.tests.conftest import client_admin, client_owner, client_user
from projects.models import Project
from rest_framework import status


@pytest.mark.django_db
def test_get_projects_admin(project: Project, client_admin):
    response = client_admin.get("/api/v1/projects/")
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json().get("results"), list)


@pytest.mark.django_db
def test_get_projects_user(project: Project, client_user):
    response = client_user.get("/api/v1/projects/")
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json().get("results"), list)


@pytest.mark.django_db
def test_get_projects_owner(project: Project, client_owner):
    response = client_owner.get("/api/v1/projects/")
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json().get("results"), list)


@pytest.mark.django_db
def test_get_project_by_id_admin(project: Project, client_admin):
    response = client_admin.get(f"/api/v1/projects/{project.id}/")
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_get_project_by_id_user(project: Project, client_user):
    response = client_user.get(f"/api/v1/projects/{project.id}/")
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_get_project_by_id_owner(project: Project, client_owner):
    response = client_owner.get(f"/api/v1/projects/{project.id}/")
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_failed_get_project_by_id_admin(project: Project, client_admin):
    response = client_admin.get(f"/api/v1/projects/aaa/")
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_failed_get_project_by_id_user(project: Project, client_user):
    response = client_user.get(f"/api/v1/projects/aaa/")
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_failed_get_project_by_id_owner(project: Project, client_owner):
    response = client_owner.get(f"/api/v1/projects/aaa/")
    assert response.status_code == status.HTTP_404_NOT_FOUND
