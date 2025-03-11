import pytest
from projects.models import Project
from rest_framework import status

from ..conftest import client, project


@pytest.mark.django_db
def test_get_projects(project: Project, client):
    response = client.get("/api/v1/projects/")
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json().get("results"), list)


@pytest.mark.django_db
def test_get_project_by_id(project: Project, client):
    response = client.get(f"/api/v1/projects/{project.id}/")
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_failed_get_project_by_id(project: Project, client):
    response = client.get(f"/api/v1/projects/aaa/")
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_create_project(project: Project, client):
    data = {"name": "Test", "description": "This is for tests"}
    response = client.post("/api/v1/projects/", data=data)
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
def test_failed_create_project(project: Project, client):
    data: dict = {}
    response = client.post("/api/v1/projects/", data=data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_update_project(project: Project, client):

    data = {
        "name": "Updated Test",
        "description": "This is an updated test",
        "owner": project.owner,
    }
    response = client.put(f"/api/v1/projects/{project.id}/", data=data, format="json")
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_failed_update_project(project: Project, client):

    data: dict = {}
    response = client.put(f"/api/v1/projects/{project.id}/", data=data, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_delete_project(project, client):
    response = client.delete(f"/api/v1/projects/{project.id}/")
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_failed_delete_project(project, client):
    response = client.delete(f"/api/v1/projects/aaa/")
    assert response.status_code == status.HTTP_404_NOT_FOUND
