import pytest
from conftest import client, project
from projects.models import Project


@pytest.mark.django_db
def test_get_projects(project: Project, client):
    response = client.get("/api/v1/projects/")
    assert response.status_code == 200
    assert isinstance(response.json().get("results"), list)


@pytest.mark.django_db
def test_get_project_by_id(project: Project, client):
    response = client.get(f"/api/v1/projects/{project.id}/")
    assert response.status_code == 200


@pytest.mark.django_db
def test_create_project(project: Project, client):
    data = {"name": "Test", "description": "This is for tests"}
    response = client.post("/api/v1/projects/", data=data)
    assert response.status_code == 201


@pytest.mark.django_db
def test_update_project(project: Project, client):

    data = {
        "name": "Updated Test",
        "description": "This is an updated test",
        "owner": project.owner,
    }
    response = client.put(f"/api/v1/projects/{project.id}/", data=data, format="json")
    assert response.status_code == 200


@pytest.mark.django_db
def test_delete_project(project, client):
    response = client.delete(f"/api/v1/projects/{project.id}/")
    assert response.status_code == 200
