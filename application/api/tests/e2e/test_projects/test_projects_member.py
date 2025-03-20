import uuid

import pytest
from api.tests.conftest import client_admin, client_owner, client_user
from projects.models import Project, ProjectMember
from rest_framework import status


@pytest.mark.django_db
@pytest.mark.parametrize(
    "client_fixture_name, expected_status, role",
    [
        ("client_admin", status.HTTP_201_CREATED, "redactor"),
        ("client_admin", status.HTTP_201_CREATED, "viewer"),
        ("client_admin", status.HTTP_400_BAD_REQUEST, "user"),
        ("client_user", status.HTTP_404_NOT_FOUND, "redactor"),
        ("client_user", status.HTTP_404_NOT_FOUND, "viewer"),
        ("client_user", status.HTTP_404_NOT_FOUND, "user"),
        ("client_owner", status.HTTP_201_CREATED, "redactor"),
        ("client_owner", status.HTTP_201_CREATED, "viewer"),
        ("client_owner", status.HTTP_400_BAD_REQUEST, "user"),
    ],
)
def test_add_member_project(
    client_fixture_name,
    expected_status,
    role,
    request,
    project: Project,
    project_member: ProjectMember,
):

    client = request.getfixturevalue(client_fixture_name)

    user = str(uuid.uuid4())

    data = {"user": user, "role": role}

    response = client.post(f"/api/v1/projects/{project.id}/members/", data=data)

    assert response.status_code == expected_status

    if response.status_code == status.HTTP_201_CREATED:
        assert ProjectMember.objects.filter(user=user).exists()


@pytest.mark.django_db
@pytest.mark.parametrize(
    "client_fixture_name, expected_status",
    [
        ("client_admin", status.HTTP_400_BAD_REQUEST),
        ("client_user", status.HTTP_404_NOT_FOUND),
        ("client_owner", status.HTTP_400_BAD_REQUEST),
    ],
)
def test_failed_add_member_project(
    client_fixture_name, expected_status, request, project: Project
):

    client = request.getfixturevalue(client_fixture_name)

    response = client.post(f"/api/v1/projects/{project.id}/members/", data={})

    assert response.status_code == expected_status
