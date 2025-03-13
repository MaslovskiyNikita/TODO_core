import pytest
from api.tests.conftest import client_admin, client_owner, client_user
from projects.models import Project
from rest_framework import status


@pytest.mark.django_db
def test_create_project_admin(project: Project, client_admin):
    data = {"name": "Test", "description": "This is for tests"}
    response = client_admin.post("/api/v1/projects/", data=data)
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
def test_create_project_user(project: Project, client_user):
    data = {"name": "Test", "description": "This is for tests"}
    response = client_user.post("/api/v1/projects/", data=data)
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
def test_create_project_owner(project: Project, client_owner):
    data = {"name": "Test", "description": "This is for tests"}
    response = client_owner.post("/api/v1/projects/", data=data)
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
def test_failed_create_project_admin(project: Project, client_admin):
    data: dict = {}
    response = client_admin.post("/api/v1/projects/", data=data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_failed_create_project_user(project: Project, client_user):
    data: dict = {}
    response = client_user.post("/api/v1/projects/", data=data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_failed_create_project_owner(project: Project, client_owner):
    data: dict = {}
    response = client_owner.post("/api/v1/projects/", data=data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
