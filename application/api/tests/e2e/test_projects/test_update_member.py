import uuid

import pytest
from api.tests.conftest import client_admin, client_owner, client_user
from projects.models import Project, ProjectMember
from rest_framework import status


@pytest.mark.django_db
@pytest.mark.parametrize(
    "client_fixture_name, expected_status, role",
    [
        ("client_admin", status.HTTP_200_OK, "redactor"),
        ("client_admin", status.HTTP_200_OK, "viewer"),
        ("client_admin", status.HTTP_400_BAD_REQUEST, "invalid_role"),
        ("client_user", status.HTTP_404_NOT_FOUND, "redactor"),
        ("client_user", status.HTTP_404_NOT_FOUND, "viewer"),
        ("client_owner", status.HTTP_200_OK, "redactor"),
        ("client_owner", status.HTTP_200_OK, "viewer"),
    ],
)
def test_update_member(
    client_fixture_name: str,
    expected_status: int,
    role: str,
    request: pytest.FixtureRequest,
    project: Project,
    project_member,
):
    client = request.getfixturevalue(client_fixture_name)

    user_uuid = project_member.id
    ProjectMember.objects.create(
        project=project_member.project, user=user_uuid, role="viewer"
    )

    data = {
        "user": user_uuid,
        "role": role,
    }

    response = client.put(
        f"/api/v1/projects/{project.id}/update_member/", data=data, format="json"
    )

    assert response.status_code == expected_status


@pytest.mark.django_db
@pytest.mark.parametrize(
    "client_fixture_name, expected_status",
    [
        ("client_admin", status.HTTP_400_BAD_REQUEST),
        ("client_user", status.HTTP_404_NOT_FOUND),
        ("client_owner", status.HTTP_400_BAD_REQUEST),
    ],
)
def test_failed_update_member(
    client_fixture_name: str,
    expected_status: int,
    request: pytest.FixtureRequest,
    project: Project,
):
    client = request.getfixturevalue(client_fixture_name)

    non_existent_user = ""
    data = {
        "user": non_existent_user,
        "role": "viewer",
    }

    response = client.put(
        f"/api/v1/projects/{project.id}/update_member/", data=data, format="json"
    )

    assert response.status_code == expected_status


@pytest.mark.django_db
@pytest.mark.parametrize(
    "client_fixture_name, expected_status",
    [
        ("client_admin", status.HTTP_400_BAD_REQUEST),
        ("client_user", status.HTTP_404_NOT_FOUND),
        ("client_owner", status.HTTP_400_BAD_REQUEST),
    ],
)
def test_failed_update_member_invalid_data(
    client_fixture_name: str,
    expected_status: int,
    request: pytest.FixtureRequest,
    project: Project,
):
    client = request.getfixturevalue(client_fixture_name)

    user_uuid = str(uuid.uuid4())
    ProjectMember.objects.create(project=project, user=user_uuid, role="viewer")

    response = client.put(
        f"/api/v1/projects/{project.id}/update_member/", data={}, format="json"
    )

    assert response.status_code == expected_status
