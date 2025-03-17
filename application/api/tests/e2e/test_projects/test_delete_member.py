import uuid

import pytest
from api.tests.conftest import client_admin, client_owner, client_user
from projects.models import Project, ProjectMember
from rest_framework import status


@pytest.mark.django_db
@pytest.mark.parametrize(
    "client_fixture_name, expected_status",
    [
        ("client_admin", status.HTTP_202_ACCEPTED),
        ("client_user", status.HTTP_404_NOT_FOUND),
        ("client_owner", status.HTTP_202_ACCEPTED),
    ],
)
def test_delete_member(
    client_fixture_name: str,
    expected_status,
    request: pytest.FixtureRequest,
    project,
    project_member,
):
    client = request.getfixturevalue(client_fixture_name)

    user_to_delete = str(uuid.uuid4())
    ProjectMember.objects.create(project=project, user=user_to_delete, role="viewer")

    response = client.delete(
        f"/api/v1/projects/{project.id}/delete_member/?user_to_delete={user_to_delete}"
    )

    assert response.status_code == expected_status


@pytest.mark.django_db
@pytest.mark.parametrize(
    "client_fixture_name, expected_status",
    [
        ("client_admin", status.HTTP_404_NOT_FOUND),
        ("client_user", status.HTTP_404_NOT_FOUND),
        ("client_owner", status.HTTP_404_NOT_FOUND),
    ],
)
def test_failed_delete_member(
    client_fixture_name: str,
    expected_status: int,
    request: pytest.FixtureRequest,
    project: Project,
):
    client = request.getfixturevalue(client_fixture_name)

    non_existent_user_uuid = str(uuid.uuid4())

    response = client.delete(
        f"/api/v1/projects/{project.id}/delete_member/{non_existent_user_uuid}/"
    )

    assert response.status_code == expected_status
